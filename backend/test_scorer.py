import json
from services.ai_service import parse_job_description, parse_resume_against_jd, init_ai
from services.ats.scorer import score_resume

# Initialize Gemini AI
from dotenv import load_dotenv
load_dotenv()
init_ai()

jd_text = """
We are looking for a Senior Frontend Developer.
Must have: 4+ years of experience, Vue.js, JavaScript, Tailwind CSS.
Nice to have: Python, Firebase.
Requires a Bachelor's degree.
"""

resume_text = """
Udit Raj

Experience: Worked from Summer 2020 to Winter 2023 (Building UI components using Vue.js and Tailwind).
Education: B.Tech in Computer Science.
Skills: Vue, JS, HTML, CSS, Python.
Frontend Engineer
"""

print("--- Testing JD Parser ---")
try:
    parsed_jd = parse_job_description(jd_text)
    print(json.dumps(parsed_jd, indent=2))
except Exception as e:
    print(f"JD Parse Failed: {e}")

print("\n--- Testing Resume Parser ---")
try:
    parsed_resume = parse_resume_against_jd(resume_text, jd_text)
    print(json.dumps(parsed_resume, indent=2))
except Exception as e:
    print(f"Resume Parse Failed: {e}")

print("\n--- Testing Final Scoring Engine ---")
try:
    # Notice we pass the raw text to score_resume, which handles the LLM calls internally now
    final_result = score_resume(resume_text, jd_text)
    print(json.dumps(final_result, indent=2))
except Exception as e:
    print(f"Scoring Failed: {e}")