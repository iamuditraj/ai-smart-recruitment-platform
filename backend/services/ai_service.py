import os
import json
import time
from groq import Groq

client = None
MODEL = "llama-3.1-8b-instant"

def init_ai():
    global client
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        client = Groq(api_key=groq_key)
        print("✅ Groq AI initialized with llama-3.1-8b-instant!")
    else:
        print("⚠️  Warning: GROQ_API_KEY not found in .env.")

def get_model():
    return client

def _call_groq_json(prompt: str) -> dict:
    if client is None:
        print("⚠️ Groq client not initialized.")
        return {}
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.1,
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            if "429" in str(e) or "rate_limit" in str(e).lower():
                if attempt < 2:
                    print(f"⚠️ Rate limit hit. Retrying in 5s... (Attempt {attempt + 1})")
                    time.sleep(5)
                    continue
            print(f"⚠️ Groq API error: {e}")
            return {}
    return {}

def parse_resume_against_jd(resume_text: str, jd_text: str) -> dict:
    prompt = f"""Analyze the following resume against the provided job description.
Return strict JSON with exactly these keys:
- "total_years_experience" (int)
- "education_tier" (int: 1=any, 2=diploma, 3=bachelor, 4=master, 5=phd)
- "latest_job_title" (str)
- "skills_found" (list of strings)
- "certifications_found" (list of strings)

Job Description:
{jd_text}

Resume:
{resume_text}

JSON only. No markdown."""
    return _call_groq_json(prompt)

def parse_job_description(jd_text: str) -> dict:
    prompt = f"""Analyze the following job description.
Return strict JSON with exactly these keys:
- "required_skills" (list of strings)
- "preferred_skills" (list of strings)
- "min_exp_years" (int)
- "education_level" (int: 1=any, 2=diploma, 3=bachelor, 4=master, 5=phd)
- "job_title" (str)
- "certifications" (list of strings)

Job Description:
{jd_text}

JSON only. No markdown."""
    return _call_groq_json(prompt)
