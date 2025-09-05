import os
import json
import re
import google.generativeai as genai
from utils.logger import logger
from dotenv import load_dotenv
load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ Gemini API Key not set. Please set GEMINI_API_KEY in your environment.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")


def _extract_json_payload(text: str) -> dict:
    """Best-effort: pull the first JSON object from a model response string."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{[\s\S]*\}", text)
        if not m:
            raise ValueError("Gemini response did not contain JSON.")
        return json.loads(m.group(0))


def optimize_resume_bundle(resume_text: str, job_description: str) -> dict:
    """
    Sends resume & JD to Gemini and returns:
      { optimized_resume, cover_letter, match_score }
    """
    prompt = f"""
You are an expert career coach and resume writer.

TASKS:
1) Rewrite and optimize the provided resume text for the given job description.
2) Write a professional, concise cover letter tailored to the same job.
3) Provide a numeric match score from 0 to 100 that reflects how well the optimized resume fits the job.

RULES:
- Keep formatting in plain text (no markdown). Use clear sections and bullet-style lines.
- Emphasize impact, metrics, and keywords from the job description.
- Keep the cover letter under 220 words, with a crisp opening and strong closing.
- Return ONLY a strict JSON object with these keys: optimized_resume, cover_letter, match_score.

RESUME TEXT:
{resume_text}

JOB DESCRIPTION:
{job_description}

JSON OUTPUT SCHEMA (STRICT):
{{
  "optimized_resume": "...",
  "cover_letter": "...",
  "match_score": 0
}}
"""
    try:
        response = model.generate_content(prompt)
        raw_text = (response.text or "").strip()
        result = _extract_json_payload(raw_text)
        # Ensure keys exist
        if "optimized_resume" not in result or "cover_letter" not in result:
            raise ValueError("Gemini JSON missing required keys.")
        # Coerce match_score
        try:
            result["match_score"] = int(result.get("match_score", 0))
        except Exception:
            result["match_score"] = 0
        return result
    except Exception as e:
        logger.error(f"Gemini API Error: {e}")
        raise
