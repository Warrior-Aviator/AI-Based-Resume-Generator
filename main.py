import os
import time
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from utils.logger import logger
from dotenv import load_dotenv
import gemini_client
import pdf_generator

load_dotenv()

app = FastAPI(title="Resume GPT")

# Serve static files (JS, CSS, images, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ensure exports folder exists for PDFs
EXPORT_DIR = os.path.join("static", "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

# Jinja2 templates
templates = Jinja2Templates(directory="templates")


# ---------- Models ----------
class OptimizeRequest(BaseModel):
    resume_text: str
    job_description: str | None = None
    template: str = "template1.html"  # template filename


# ---------- Routes ----------
@app.get("/", response_class=HTMLResponse)
async def serve_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/optimize-resume")
async def optimize_resume(data: OptimizeRequest):
    """Optimize resume & generate cover letter + job match score using Gemini API."""
    try:
        jd = data.job_description.strip() if data.job_description else ""
        if not jd:
            jd = (
                "No specific job description provided. Optimize the resume for a "
                "strong, general-purpose professional software engineering profile."
            )

        optimized_data = gemini_client.optimize_resume_bundle(
            data.resume_text, jd
        )
        # Also echo back the selected template so the FE can preview
        optimized_data["template"] = data.template
        return JSONResponse(content=optimized_data)

    except Exception as e:
        logger.error(f"Error optimizing resume: {str(e)}")
        return JSONResponse(content={"error": "Something went wrong"}, status_code=500)


@app.post("/generate-pdf")
async def generate_pdf(resume_text: str = Form(...), cover_letter: str = Form(...)):
    """Generate a PDF file for optimized resume & cover letter and return a downloadable path."""
    try:
        pdf_bytes = pdf_generator.create_pdf(resume_text, cover_letter)
        filename = f"resume_{int(time.time())}.pdf"
        pdf_path = os.path.join(EXPORT_DIR, filename)
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)
        # Return a direct file path for the frontend to open
        return {"pdf_path": f"/static/exports/{filename}"}
    except Exception as e:
        logger.error(f"PDF generation failed: {str(e)}")
        return JSONResponse(content={"error": "Failed to generate PDF"}, status_code=500)


@app.post("/preview", response_class=HTMLResponse)
async def preview_resume(request: Request, template: str = Form(...),
                         name: str = Form("Candidate Name"),
                         contact_info: str = Form("Email: candidate@example.com | Phone: 1234567890"),
                         summary: str = Form(""), education: str = Form(""),
                         experience: str = Form(""), projects: str = Form(""),
                         skills: str = Form(""), hobbies: str = Form(""),
                         achievements: str = Form(""), cover_letter: str = Form("")):
    """Render a preview page with the chosen template."""
    return templates.TemplateResponse(template, {
        "request": request,
        "name": name,
        "contact_info": contact_info,
        "summary": summary,
        "education": education,
        "experience": experience,
        "projects": projects,
        "skills": skills,
        "hobbies": hobbies,
        "achievements": achievements,
        "cover_letter": cover_letter,
    })


@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Resume GPT API started successfully!")
