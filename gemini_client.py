import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import re

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_optimized_resume(resume_text: str, job_description: str) -> dict:
    prompt = f"""
You are a resume optimization assistant.

Given the following:
Resume:
{resume_text}

Job Description:
{job_description}

Generate:
1. An optimized version of the resume tailored to the job.
2. A tailored cover letter.

Format the response in pure JSON like this:
{{
  "optimized_resume": "<Optimized resume here>",
  "tailored_cover_letter": "<Tailored cover letter here>"
}}
Only output the JSON. Do not include any explanation or markdown formatting.
"""

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    result_text = response.text.strip()
    
    # 🔍 Add this log to see the raw Gemini output
    print("==== GEMINI RAW OUTPUT ====")
    print(result_text[:1000])  # Print first 1000 chars

    try:
        # Strip markdown if needed
        if result_text.startswith("```json"):
            result_text = result_text[7:].strip("` \n")
        elif result_text.startswith("```"):
            result_text = result_text[3:].strip("` \n")

        return json.loads(result_text)
    
    except Exception as e:
        raise ValueError(f"Failed to parse Gemini response as JSON: {e}")
