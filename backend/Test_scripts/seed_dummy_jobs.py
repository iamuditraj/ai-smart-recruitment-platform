import os
import sys
# Ensure the backend directory is in the Python path
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BACKEND_DIR)

from dotenv import load_dotenv
load_dotenv(os.path.join(BACKEND_DIR, '.env'))

from firebase_admin import firestore
from services.firebase_service import init_firebase, get_db



def seed_jobs(seed_data, email):
    # Initialize Firebase using your existing service
    init_firebase()
    db = get_db()
    if not db:
        print("Failed to initialize Firebase. Make sure 'serviceAccountKey.json' is present.")
        return



    if not seed_data:
        print("No dummy jobs to seed right now. Add data to DUMMY_JOBS list.")
        return

    # Iterate over given list of dummy jobs and post them
    for job_info in seed_data:
        try:
            job_ref = db.collection('jobs').document()
            job_data = {
                "id": job_ref.id,
                "title": job_info.get("title", "Untitled Job"),
                "company": job_info.get("company", "Test Company"),
                "department": job_info.get("department", ""),
                "location": job_info.get("location", "Remote"),
                "workArrangement": job_info.get("workArrangement", "Remote"),
                "type": job_info.get("type", "Full-time"),
                "experienceLevel": job_info.get("experienceLevel", "Mid-Level"),
                "salary": job_info.get("salary", "Competitive"),
                "companyOverview": job_info.get("companyOverview", ""),
                "jobSummary": job_info.get("jobSummary", ""),
                "keyResponsibilities": job_info.get("keyResponsibilities", ""),
                "requiredSkills": job_info.get("requiredSkills", ""),
                "softSkills": job_info.get("softSkills", ""),
                "educationalBackground": job_info.get("educationalBackground", ""),
                "preferredQualifications": job_info.get("preferredQualifications", ""),
                "applicationDeadline": job_info.get("applicationDeadline", ""),
                "requiredDocumentsList": job_info.get("requiredDocumentsList", []),
                "recruiter_email": email,
                "posted_at": firestore.SERVER_TIMESTAMP
            }
            # Set data in the random document reference created
            job_ref.set(job_data)
            print(f"Successfully seeded job: {job_data['title']} (ID: {job_data['id']})")
        except Exception as e:
            print(f"Error seeding job '{job_info.get('title', 'Unknown')}': {e}")

if __name__ == "__main__":
    RECRUITER_EMAIL = "recruiter1@test.com"
    
    # The dummy data to seed will be given later. 
    # For now, it's just an empty array or you can fill it with dictionaries.
    DUMMY_JOBS = [
        {
            "title": "Full Stack Developer",
            "company": "NexaCloud Solutions",
            "department": "Engineering",
            "location": "Bangalore, India",
            "workArrangement": "Hybrid",
            "type": "Full-time",
            "experienceLevel": "Mid-Level",
            "salary": "₹12-18 LPA",
            "companyOverview": "NexaCloud Solutions is a fast-growing SaaS company building cloud-native enterprise tools for the Indian market.",
            "jobSummary": "We are looking for a Full Stack Developer to build and maintain scalable web applications using React and Node.js. You will work closely with product and design teams to deliver high-quality features.",
            "keyResponsibilities": "Develop and maintain frontend components using React. Build RESTful APIs using Node.js and Express. Write unit and integration tests. Participate in code reviews and agile ceremonies. Optimize applications for performance and scalability.",
            "requiredSkills": "React, Node.js, JavaScript, REST APIs, MongoDB, Git, HTML, CSS",
            "softSkills": "Team collaboration, communication, problem solving",
            "educationalBackground": "Bachelor's degree in Computer Science or related field",
            "preferredQualifications": "Experience with TypeScript, Docker, AWS, or CI/CD pipelines. Prior startup experience is a plus.",
            "applicationDeadline": "2025-05-31",
            "requiredDocumentsList": ["Resume", "Cover Letter"]
        },
        {
            "title": "Machine Learning Engineer",
            "company": "DataMinds AI",
            "department": "AI Research",
            "location": "Hyderabad, India",
            "workArrangement": "Remote",
            "type": "Full-time",
            "experienceLevel": "Senior",
            "salary": "₹20-30 LPA",
            "companyOverview": "DataMinds AI is an AI-first company building intelligent automation products for enterprise clients across finance and healthcare sectors.",
            "jobSummary": "We need an experienced ML Engineer to design, train, and deploy machine learning models at scale. You will own the full ML lifecycle from data preprocessing to production deployment.",
            "keyResponsibilities": "Design and implement ML models for classification, regression, and NLP tasks. Build data pipelines using Python and Apache Spark. Deploy models using Docker and Kubernetes. Monitor model performance and retrain as needed. Collaborate with data engineers and product managers.",
            "requiredSkills": "Python, Machine Learning, scikit-learn, TensorFlow or PyTorch, SQL, Docker, Git",
            "softSkills": "Analytical thinking, attention to detail, self-driven",
            "educationalBackground": "Bachelor's or Master's degree in Computer Science, Statistics, or related field",
            "preferredQualifications": "Experience with NLP, LLMs, MLflow, Kubernetes, or AWS SageMaker. Publications or open source contributions are a strong plus.",
            "applicationDeadline": "2025-06-15",
            "requiredDocumentsList": ["Resume", "GitHub Profile"]
        },
        {
            "title": "Backend Developer",
            "company": "FinEdge Technologies",
            "department": "Platform Engineering",
            "location": "Mumbai, India",
            "workArrangement": "On-site",
            "type": "Full-time",
            "experienceLevel": "Mid-Level",
            "salary": "₹10-16 LPA",
            "companyOverview": "FinEdge Technologies is a fintech startup building next-generation payment infrastructure and lending platforms for retail banks.",
            "jobSummary": "We are hiring a Backend Developer to build robust, secure, and high-performance APIs for our core banking and payments platform.",
            "keyResponsibilities": "Design and develop microservices using Python and Flask or FastAPI. Integrate third-party payment gateways and banking APIs. Write secure, well-tested backend code. Manage PostgreSQL databases and write optimized queries. Work in an agile team with weekly sprints.",
            "requiredSkills": "Python, Flask, REST APIs, PostgreSQL, Git, Linux, SQL",
            "softSkills": "Accountability, attention to detail, ability to work under pressure",
            "educationalBackground": "Bachelor's degree in Computer Science, IT, or equivalent",
            "preferredQualifications": "Experience with FastAPI, Redis, Kafka, or microservices architecture. Prior fintech or banking domain experience preferred.",
            "applicationDeadline": "2025-05-20",
            "requiredDocumentsList": ["Resume"]
        },
        {
            "title": "Data Analyst",
            "company": "RetailIQ",
            "department": "Business Intelligence",
            "location": "Pune, India",
            "workArrangement": "Hybrid",
            "type": "Full-time",
            "experienceLevel": "Entry-Level",
            "salary": "₹5-8 LPA",
            "companyOverview": "RetailIQ is a retail analytics company helping e-commerce and brick-and-mortar businesses make data-driven decisions through dashboards and predictive insights.",
            "jobSummary": "We are looking for a Data Analyst to turn raw business data into actionable insights. You will build dashboards, run analysis, and present findings to business stakeholders.",
            "keyResponsibilities": "Collect, clean, and analyze large datasets using Python and SQL. Build dashboards and reports in Power BI or Tableau. Identify trends and patterns in sales, customer, and inventory data. Present findings to non-technical stakeholders. Collaborate with engineering to improve data pipelines.",
            "requiredSkills": "Python, SQL, Excel, Data Visualization, Pandas, Power BI or Tableau",
            "softSkills": "Communication, storytelling with data, curiosity",
            "educationalBackground": "Bachelor's degree in Statistics, Mathematics, Computer Science, or related field",
            "preferredQualifications": "Familiarity with machine learning concepts, Google Analytics, or retail domain knowledge.",
            "applicationDeadline": "2025-05-25",
            "requiredDocumentsList": ["Resume", "Cover Letter"]
        },
        {
            "title": "DevOps Engineer",
            "company": "CloudNest Infrastructure",
            "department": "Infrastructure & Reliability",
            "location": "Delhi, India",
            "workArrangement": "Remote",
            "type": "Full-time",
            "experienceLevel": "Senior",
            "salary": "₹18-25 LPA",
            "companyOverview": "CloudNest Infrastructure provides managed cloud services and DevOps consulting to mid-sized tech companies across South Asia.",
            "jobSummary": "We need a senior DevOps Engineer to own our CI/CD pipelines, cloud infrastructure, and reliability engineering. You will work across multiple client environments and internal platforms.",
            "keyResponsibilities": "Design and maintain CI/CD pipelines using GitHub Actions or Jenkins. Manage AWS or GCP infrastructure using Terraform. Monitor system health using Prometheus and Grafana. Implement security best practices and compliance checks. Mentor junior engineers and document infrastructure decisions.",
            "requiredSkills": "Docker, Kubernetes, AWS, Terraform, CI/CD, Linux, Git, Bash scripting",
            "softSkills": "Ownership mindset, proactive communication, documentation discipline",
            "educationalBackground": "Bachelor's degree in Computer Science or IT",
            "preferredQualifications": "AWS or GCP certifications, experience with Helm, Ansible, or multi-cloud environments.",
            "applicationDeadline": "2025-06-01",
            "requiredDocumentsList": ["Resume"]
        }
    ]
    
    print("Starting job seeding process...")
    seed_jobs(DUMMY_JOBS, RECRUITER_EMAIL)
    print("Job seeding process finished.")
