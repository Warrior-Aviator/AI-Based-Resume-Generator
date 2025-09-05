from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from gemini_client import generate_optimized_resume
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Enable CORS (optional but safe here)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

class ResumeRequest(BaseModel):
    resume_text: str
    job_description: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/optimize-resume")
async def optimize_resume(request: ResumeRequest):
    try:
        optimized_result = generate_optimized_resume(request.resume_text, request.job_description)
        return JSONResponse(content=optimized_result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Optional: run if this is the main file
if __name__ == "__main__":
    uvicorn.run("resume:app", reload=True)
