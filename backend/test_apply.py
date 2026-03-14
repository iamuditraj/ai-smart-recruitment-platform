import requests
import json

url = "http://localhost:5001/api/jobs/apply"

# Let's write a quick dummy python resume focusing on the JD's requirements: React, Node.js, PostgreSQL
resume_content = """
Candidate Name: John Doe
Email: candidev@example.com
Summary: Full Stack Developer with 4 years of experience building web applications.
Skills: React, Node.js, Express, PostgreSQL, JavaScript, Python
Experience:
- Software Engineer at Tech Corp (4+ years of professional experience)
  - Built microservices in Node.js and user interfaces in React.
  - Managed a PostgreSQL database.
Education: Bachelor's degree in Computer Science
"""

with open("test_candi_resume.txt", "w") as f:
    f.write(resume_content)

files = { "resume": ("test_candi_resume.txt", open("test_candi_resume.txt", "rb")) }
data = {
    "job_id": "uORoxCyMVJvhdvObL1Vu", # Full Stack Developer job 
    "candidate_email": "candidev@example.com"
}

response = requests.post(url, files=files, data=data)

print(json.dumps(response.json(), indent=2))
