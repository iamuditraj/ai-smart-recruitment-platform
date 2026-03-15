import requests

url = "http://localhost:5001/api/analyze"
data = {"jobDescription": "We need a Python developer with 3 years experience in Flask, PostgreSQL, and Docker."}
files = {"resumes": ("test_resume.txt", open("test_resume.txt", "rb"))}

response = requests.post(url, data=data, files=files)
print(response.json())
