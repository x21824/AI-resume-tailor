import sys
import os
import streamlit as st
from docx import Document
from openai import OpenAI
import asyncio
from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv
import tiktoken

load_dotenv()

# Windows-specific asyncio fix
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Resume Extraction
def extract_resume_text(docx_file):
    doc = Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip() != ""])

# Crawl website for job description in markdown
async def crawl_url(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url)
        return result.markdown, result.success

# Count actual tokens using tiktoken
def count_tokens(text, model="gpt-3.5-turbo"):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))

# Tailor resume using OpenAI
def tailor_resume_with_openai(resume_text, job_description):
    model = "gpt-3.5-turbo"
    max_total_tokens = 16000
    max_output_tokens = 1530

    prompt_static = (
        "You are an expert resume editor. Given a resume and a job description, your task is to enhance the formatting, structure, and keyword alignment of the resume to better fit the job description. Provide only a resume as an output.\n"
        "\n"
        "Instructions:\n"
        "- You may reasonably infer duties and baseline competencies based on the applicant's job titles and typical expectations for those roles in their industry.\n"
        "- If a job posting asks for responsibilities that are logically implied by the applicant’s roles (e.g., supervising staff, using Git, managing compliance, etc.), you may reflect that in the resume — but only if the base role strongly suggests it.\n"
        "- Do NOT fabricate or exaggerate certifications, employers, or achievements.\n"
        "- Exclude duties not needed in the job description, even if the applicant likely performed them.\n"
        "- Use a clear resume format with sections like Summary, Skills, Experience, and Education.\n"
        "- Format the output professionally with headers and bullet points.\n"
        "- Do NOT copy or repeat parts of the job description in the output.\n"
        "- Do not include job responsibilities, qualifications, or posting URLs directly.\n"
        "- Only tailor the resume content based on the applicant's background.\n"
        "- Do NOT include commentary, summaries, or messages directed at the user. Only output the tailored resume content.\n"
        "- Do NOT include any closing remarks like “let me know” or “thank you.” End strictly with the last resume section (e.g., Certifications, Skills, etc.).\n"
        "- Do NOT include any contact info at the bottom. The contact info is already listed at the top and should not be repeated or rephrased. Do not end with “Contact me,” “Visit,” or any closing call-to-action.\n"
        "- Under no circumstance should the output end with any sentence that includes “contact,” “reach out,” “let me know,” “visit,” or any variation of a closing remark. The resume must end cleanly at the last formal section such as Certifications, Skills, or Education.\n"
        "\nResume:\n"
    )

    prompt_tokens = count_tokens(prompt_static, model)
    resume_tokens = count_tokens(resume_text, model)
    available_for_job_desc = max_total_tokens - (resume_tokens + prompt_tokens + max_output_tokens)

    job_words = job_description.split()
    trimmed_job = job_description
    while count_tokens(trimmed_job, model) > available_for_job_desc and len(job_words) > 100:
        job_words = job_words[:-100]
        trimmed_job = " ".join(job_words)

    prompt = f"{prompt_static}{resume_text}\n\nJob Description:\n{trimmed_job}\n\nTailored Resume:".strip()

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=max_output_tokens,
    )
    return response.choices[0].message.content
# causing issues with output, commented out cos might need it in the future
# def trim_after_last_section(text):
#     lines = text.strip().splitlines()
#     cutoff_keywords = ["certifications", "skills", "education", "experience", "summary"]
#     last_good_line = 0
#     for i, line in enumerate(lines):
#         if any(kw in line.strip().lower() for kw in cutoff_keywords):
#             last_good_line = i
#     return "\n".join(lines[:last_good_line+1]).strip()


# UI
st.title("AI-Powered Resume Enhancer")
resume_file = st.file_uploader("Upload your resume (.docx)", type="docx")
base_url = st.text_input("Enter the job posting's URL")

if st.button("Start Processing"):
    if resume_file and base_url:
        with st.spinner("Processing resume..."):
            resume_text = extract_resume_text(resume_file)
            markdown_text, success = asyncio.run(crawl_url(base_url))

            if not success or not markdown_text.strip():
                st.error("Failed to crawl job description from the provided URL.")
            else:
                tailored = tailor_resume_with_openai(resume_text, markdown_text)
                st.success("Tailored Resume Generated:")
                # this garbage line below cuts off the generation, since it tries to work on separating by section, also by commenting out this, the 'contact me for more info' and other user-directed comments for the user stopped appearing, idk why but it works.
                # trimmed_resume = trim_after_last_section(tailored)
                st.text_area("Tailored Resume", tailored, height=500)

    else:
        st.warning("Please upload a resume and enter a URL.")