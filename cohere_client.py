import os
import cohere
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("COHERE_API_KEY")

co = cohere.Client(api_key)

def generate_optimized_resume(resume_text: str, job_description: str) -> dict:
    system_prompt = """
You are an AI resume assistant.

Your task is to:
1. Optimize the given resume for the job description.
2. Generate a tailored cover letter.

Respond in **valid JSON** like this:
{
  "optimized_resume": "...",
  "tailored_cover_letter": "..."
}

Only output the JSON. No commentary.
"""

    user_prompt = f"""Resume:
{resume_text}

Job Description:
{job_description}
"""

    try:
        response = co.chat(
            model="command-r-plus",  # ✅ Chat-compatible model
            temperature=0.7,
            message=user_prompt,
            preamble=system_prompt,
        )

        text_output = response.text.strip()

        print("=== Raw Cohere Output ===")
        print(text_output[:1000])

        if text_output.startswith("```json"):
            text_output = text_output[7:].strip("` \n")
        elif text_output.startswith("```"):
            text_output = text_output[3:].strip("` \n")

        return json.loads(text_output)

    except Exception as e:
        raise ValueError(f"Failed to parse Cohere chat response: {e}")
