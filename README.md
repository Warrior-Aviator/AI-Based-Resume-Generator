# 🚀 Resume GPT 
is a FastAPI + Jinja2 web app that helps you optimize resumes and generate tailored cover letters using AI.
It analyzes your existing resume and the target job description, then produces:

✨ An optimized resume with improved phrasing

📝 A tailored cover letter

📊 A match score showing how well your resume fits the job

The app also allows PDF downloads with different templates, and supports multiple AI providers (Gemini, Cohere, Hugging Face, OpenAI, etc.) to avoid quota issues.

# 📌 Features

✅ Resume Optimization → Polishes your resume with AI

✅ Cover Letter Generation → Auto-drafted based on your JD

✅ Match Score → Percentage fit for the given job description

✅ PDF Export → Choose from multiple professional templates

✅ Multi-Model Support → Gemini, Cohere, Hugging Face, OpenAI (fallbacks)

✅ Live Preview → View optimized text before downloading

✅ Error Handling → Friendly messages for quota limits or API errors

# 🛠️ Tech Stack

Backend: FastAPI

Frontend: Jinja2 + Vanilla JS + CSS

AI Models: Google Gemini, Cohere, Hugging Face, OpenAI (optional)

PDF Generation: WeasyPrint

Styling: Custom CSS

# 📂 Project Structure
Resume-GPT/
│── main.py               # FastAPI app entry
│── gemini_client.py      # Gemini API wrapper
│── cohere_client.py      # Cohere API wrapper (optional)
│── templates/            # Jinja2 templates
│   ├── index.html
│   ├── resume_template1.html
│   ├── resume_template2.html
│   ├── resume_template3.html
│── static/               # CSS + JS
│   ├── style.css
│   ├── script.js
│── requirements.txt      # Python dependencies
│── .env                  # API keys (not committed to GitHub!)
│── README.md             # Documentation

# ⚙️ Installation
1. Clone the repo
git clone https://github.com/your-username/Resume-GPT.git
cd Resume-GPT

2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3. Install dependencies
pip install -r requirements.txt

4. Set up API keys

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key
COHERE_API_KEY=your_cohere_api_key   # optional
HF_API_KEY=your_huggingface_api_key  # optional
OPENAI_API_KEY=your_openai_api_key   # optional

5. Run the app
uvicorn main:app --reload

Open your browser → http://127.0.0.1:8000

# 🚀 API Providers & Free Plans
Provider	Free Tier	Notes
Gemini	Limited quota/day	Best results, but strict rate limits
Cohere	100 requests/day	Reliable backup option
Hugging Face	30k tokens/month	Lots of open LLMs
OpenAI	$5 free credits (3 months)	After that → paid

The app lets you switch providers if one hits a quota limit (429 error).

# 📌 To-Do (Future Enhancements)

 Save resume history in SQLite

 Dark / Light theme toggle

 Keyword highlighting from JD in resume

 Export to DOCX in addition to PDF

 Mobile-friendly UI

# 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first to discuss what you’d like to change.

# 📜 License

This project is licensed under the MIT License.
