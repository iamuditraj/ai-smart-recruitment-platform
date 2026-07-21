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

# TODO: replace with open source model
def _run_inference(prompt: str) -> dict:
    fallback = {
        "required_skills": [],
        "preferred_skills": [],
        "min_exp_years": 0,
        "education_level": 1,
        "job_title": "",
        "certifications": [],
        "skills_found": [],
        "total_years_experience": 0,
        "education_tier": 1,
        "latest_job_title": ""
    }

    if client is None:
        print("⚠️ Groq client not initialized.")
        print("⚠️ Groq unavailable — using fallback defaults")
        return fallback

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
            break

    print("⚠️ Groq unavailable — using fallback defaults")
    return fallback

def parse_resume(resume_text: str, jd_text: str = None) -> dict:
    """Parse a resume into structured data.

    When *jd_text* is provided the prompt also asks the LLM for
    ``skills_found`` (skills matching the JD) which the ATS scorer needs.
    Temperature is always 0.1 (via ``_run_inference``) for consistent scoring.
    """
    jd_context = ""
    skills_found_field = ""
    if jd_text:
        jd_context = f"\nJob Description:\n{jd_text}\n"
        skills_found_field = '- "skills_found": (list of strings) specifically those that match or are relevant to the JD\n'

    prompt = f"""Analyze the following resume{' in the context of the provided job description' if jd_text else ''}.
Extract the candidate's professional profile into a detailed JSON format.

Return strict JSON with exactly these keys:
- "name": (str) Candidate's full name
- "email": (str)
- "phone": (str)
- "summary": (str) A brief professional summary
- "total_years_experience": (int) Total years of work history
- "education_tier": (int: 1=any, 2=diploma, 3=bachelor, 4=master, 5=phd)
- "latest_job_title": (str)
- "skills": (list of strings) All skills found in the resume
- "experience": (list of objects) Each object must have: "title", "company", "duration", "description"
- "education": (list of objects) Each object must have: "degree", "institution", "year"
- "certifications": (list of strings)
- "languages": (list of strings)
{skills_found_field}
{jd_context}
Resume content:
{resume_text}

Return ONLY the JSON object. No other text."""
    return _run_inference(prompt)


def parse_resume_against_jd(resume_text: str, jd_text: str) -> dict:
    """Convenience wrapper — always includes JD context for ATS scoring."""
    return parse_resume(resume_text, jd_text=jd_text)

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
    return _run_inference(prompt)
