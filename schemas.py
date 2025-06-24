from pydantic import BaseModel

class ResumeRequest(BaseModel):
    resume_text: str
    job_description: str

class DownloadRequest(BaseModel):
    resume_text: str
    cover_letter: str
