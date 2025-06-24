from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import io
from models.schemas import ResumeRequest, DownloadRequest
#from gemini_client import generate_optimized_resume
from cohere_client import generate_optimized_resume 

from pdf_generator import generate_pdf
from utils.logger import logger

from fastapi.staticfiles import StaticFiles
import os

import traceback  # add at top of main.py if not already

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")  # ✅ This serves static files

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/optimize-resume")


@app.post("/optimize-resume")
async def optimize_resume(request: ResumeRequest):
    try:
        result = generate_optimized_resume(request.resume_text, request.job_description)
        return JSONResponse(content={"optimized_output": result})
    except Exception as e:
        print("==== INTERNAL SERVER ERROR ====")
        traceback.print_exc()  # prints full error details to terminal
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/download-pdf")
async def download_pdf(data: DownloadRequest):
    try:
        logger.info("Generating PDF...")
        pdf_bytes = generate_pdf(data.resume_text, data.cover_letter)
        return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf", headers={
            "Content-Disposition": "attachment; filename=Optimized_Resume.pdf"
        })
    except Exception as e:
        logger.error(f"Error generating PDF: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
