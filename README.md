# AI-Powered Resume Tailor

This tool uses AI to help job seekers instantly tailor their resumes to job postings. Built with Streamlit, it allows users to upload their `.docx` resume and paste a job post URL. The tool uses GPT-3.5-turbo to rewrite the resume to align with the job's requirements cleanly, professionally, and without fluff.

## ✨ Features

- Upload resume in `.docx` format
- Paste any job URL
- Automatically scrapes and cleans job descriptions
- Uses GPT-3.5 to rewrite your resume to match the job
- Displays a clean, formatted draft with no commentary or fluff

## 📦 Tech Stack

- Python + Streamlit
- OpenAI GPT-3.5 API
- `crawl4ai` + Playwright (job scraping)
- `python-docx` (resume parsing)
- `tiktoken` (token control)

## 🚀 Setup & Installation

1. Clone this repo

   git clone https://github.com/x21824/AI-resume-tailor.git

2. Install dependencies

   pip install -r requirements.txt
   playwright install

3. Add your OpenAI API key in a `.env` file:

   OPENAI_API_KEY=your-key-here

4. Run the app

   streamlit run code.py

## 🛠 How It Works

1. Upload a `.docx` resume.
2. Paste a URL from a job posting.
3. Click **Start Processing**.
4. The AI compares your resume to the job description and rewrites it.
5. Scroll down to view your AI-generated resume.

## 📄 Presentation

Check out the full project walkthrough in the `presentation.pptx`.

## ⚠️ Limitations

- Trims job descriptions to avoid token overflows.
- Some sites may not scrape properly (crawler returns Markdown).
- No file exports or session saving (yet).
- Windows-specific async fix required.

## 🧠 Future Improvements

- Export as downloadable `.docx`
- Add cover letter generator
- Batch job URL support
- Relevance scoring and highlighting
- UI upgrades & privacy features

> This project is part of an SDLC + AI workshop by [baraa shullar](https://github.com/x21824). Feel free to fork and expand!

## 🧪 How to Use

1. Make sure you have Python 3.8+ and pip installed.
2. Install required Python packages:

pip install streamlit python-docx openai crawl4ai tiktoken python-dotenv
playwright install

3. Create a `.env` file and insert your OpenAI key:

OPENAI_API_KEY=your_key_here

4. Launch the app:

streamlit run code.py

5. Upload your resume (`.docx`) and paste a job posting URL.
6. Click "Start Processing" and wait for the AI to generate your tailored resume.
7. Scroll to view and copy the output.
