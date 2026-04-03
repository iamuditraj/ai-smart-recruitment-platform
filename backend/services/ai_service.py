import os
import json
import time
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

model = None

def init_ai():
    global model
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        print("✅ Gemini AI initialized!")
    else:
        print("⚠️  Warning: GEMINI_API_KEY not found in .env.")

def get_model():
    return model

def parse_resume_against_jd(resume_text: str, jd_text: str) -> dict:
    if model is None:
        print("⚠️ Warning: Model not initialized or missing API key.")
        return {}

    prompt = f"""
Analyze the following resume against the provided job description.
Return strict JSON containing exactly these keys:
- "total_years_experience" (int: calculated from date ranges)
- "education_tier" (int: 1=any, 2=diploma, 3=bachelor, 4=master, 5=phd)
- "latest_job_title" (str)
- "skills_found" (list of strings: normalize these against the JD)
- "certifications_found" (list of strings)

Job Description:
{jd_text}

Resume:
{resume_text}
"""
    try:
        response_text = None
        for attempt in range(3):
            try:
                response = model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        response_mime_type="application/json"
                    )
                )
                response_text = response.text
                break
            except Exception as e:
                if isinstance(e, ResourceExhausted) or '429' in str(e):
                    if attempt < 2:
                        print(f"⚠️ Warning: Rate limit hit. Retrying in 6 seconds... (Attempt {attempt + 1})")
                        time.sleep(6)
                        continue
                raise
        return json.loads(response_text)
    except json.JSONDecodeError:
        print("⚠️ Error: Failed to parse JSON response from Gemini.")
        return {}
    except Exception as e:
        print(f"⚠️ Error during Gemini API call: {e}")
        return {}

def parse_job_description(jd_text: str) -> dict:
    if model is None:
        print("⚠️ Warning: Model not initialized or missing API key.")
        return {}

    prompt = f"""
Analyze the following job description.
Return strict JSON containing exactly these keys:
- "required_skills" (list of strings)
- "preferred_skills" (list of strings)
- "min_exp_years" (int)
- "education_level" (int: 1=any, 2=diploma, 3=bachelor, 4=master, 5=phd)
- "job_title" (str)
- "certifications" (list of strings)

Job Description:
{jd_text}
"""
    try:
        response_text = None
        for attempt in range(3):
            try:
                response = model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        response_mime_type="application/json"
                    )
                )
                response_text = response.text
                break
            except Exception as e:
                if isinstance(e, ResourceExhausted) or '429' in str(e):
                    if attempt < 2:
                        print(f"⚠️ Warning: Rate limit hit. Retrying in 6 seconds... (Attempt {attempt + 1})")
                        time.sleep(6)
                        continue
                raise
        return json.loads(response_text)
    except json.JSONDecodeError:
        print("⚠️ Error: Failed to parse JSON response from Gemini.")
        return {}
    except Exception as e:
        print(f"⚠️ Error during Gemini API call: {e}")
        return {}
