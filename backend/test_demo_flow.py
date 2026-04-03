import os
import json
from dotenv import load_dotenv

# 1. Force Python to read your .env file
load_dotenv()

# 2. NOW import the services (which will now see the API key)
from services.ai_service import parse_job_description, parse_resume_against_jd, init_ai
from services.ats.scorer import score_resume

# Initialize the Gemini model for the test
init_ai()


jd_text = """
We are looking for a Senior Frontend Developer.
Must have: 4+ years of experience, Vue.js, JavaScript, Tailwind CSS.
Nice to have: Python, Firebase.
Requires a Bachelor's degree.
"""

resume_text = """
Udit Raj
Frontend Engineer
Experience: Aug 2019 - Present (Building UI components using Vue.js and Tailwind).
Education: B.Tech in Computer Science.
Skills: Vue, JS, HTML, CSS, Python.
"""

print("--- STEP 1: Pre-Parsing Job Description (Simulating /api/parse-jd) ---")
# This represents you uploading the JD hours before the presentation
parsed_jd = parse_job_description(jd_text)
print("✅ JD Parsed Successfully:")
print(json.dumps(parsed_jd, indent=2))

print("\n--- STEP 2: Processing Resume (Simulating /api/score-resume) ---")
# This represents clicking "Score Resume" on stage
parsed_resume = parse_resume_against_jd(resume_text, jd_text)
print("✅ Resume Parsed Successfully:")
print(json.dumps(parsed_resume, indent=2))

print("\n--- STEP 3: Final Decoupled Scoring ---")
# The math logic now runs safely on the two cached dictionaries
final_result = score_resume(parsed_resume, parsed_jd, resume_text)
print("✅ Scoring Complete:")
print(json.dumps(final_result, indent=2))

print("\n--- STEP 4: Stress Testing the 429 Safety Net ---")
print("Firing 5 rapid API requests to purposely trigger the rate limit...")
for i in range(5):
    print(f"\n[Test {i+1}/5] Pinging Gemini...")
    try:
        # Pinging the API rapidly to force the burst limit
        test_parse = parse_resume_against_jd(resume_text, jd_text)
        print(f"✅ Success without hitting limit!")
    except Exception as e:
        print(f"❌ Failed: {e}")
        
print("\n🎉 Demo test script complete.")