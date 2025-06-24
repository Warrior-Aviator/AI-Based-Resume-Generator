# AI-Based-Resume-Generator

# 🧠 AI Resume Optimizer

An intelligent, full-stack web application that **optimizes resumes and generates tailored cover letters** based on a provided job description using **Cohere’s large language model**. The tool leverages machine learning to help job seekers craft better applications in seconds.

## 🔍 Features

- ✨ Optimize your existing resume to match the job role
- 📄 Auto-generate a personalized cover letter
- 🧠 Powered by Cohere’s language model (Chat API)
- 📥 Download results as a clean, printable PDF
- 🌐 Simple, responsive web interface built using **HTML, CSS, JavaScript, and FastAPI**

---

## 🚀 Demo

1. Paste your resume
2. Paste the job description
3. Click **Optimize**
4. View and download:
   - Optimized Resume ✅
   - Tailored Cover Letter ✅

---

## 🏗️ Project Structure

├── main.py # FastAPI backend (API endpoints)
├── cohere_client.py # Calls Cohere API to generate optimized content
├── pdf_generator.py # Generates PDF using WeasyPrint
├── resume.py # Optional UI route handler
├── templates/
│ └── index.html # Main web UI (form and results)
├── static/
│ ├── style.css # CSS for styling
│ └── script.js # (Optional) JS interactions (if used separately)
├── .env # Stores your API key (GEMINI_API_KEY or COHERE_API_KEY)
└── README.md # You are here

yaml
Copy
Edit

---

## ⚙️ How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/resume-optimizer.git
cd resume-optimizer

2. Set Up Environment
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Create a .env file:

ini
Copy
Edit
COHERE_API_KEY=your_actual_api_key
3. Run the App
bash
Copy
Edit
uvicorn main:app --reload
Visit http://127.0.0.1:8000 in your browser.

📦 Requirements
Python 3.8+

FastAPI

Cohere Python SDK

WeasyPrint

Install manually:

bash
Copy
Edit
pip install fastapi uvicorn python-dotenv cohere weasyprint
🧠 Powered By
Cohere Command R+ Chat API

FastAPI

HTML/CSS/JS frontend

WeasyPrint (for generating PDFs)

📌 Future Enhancements
Job match score visualizer (e.g., 84% fit)

Export optimized history

Login/Save for future reference

Add support for multiple languages
