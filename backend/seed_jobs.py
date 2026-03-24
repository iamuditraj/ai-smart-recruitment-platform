"""
seed_jobs.py
============
Registers recruiter1@test.com … recruiter5@test.com (if not already present)
and posts one unique CS-domain job per recruiter via the Flask REST API.

Usage (with the backend running on port 5001):
    python seed_jobs.py

Optional env var:
    BASE_URL  – override the default http://localhost:5001
"""

import sys
import requests
import json

BASE_URL = "http://localhost:5001"

# ---------------------------------------------------------------------------
# 5 unique CS job definitions – one per recruiter
# ---------------------------------------------------------------------------
JOBS = [
    {
        # recruiter1@test.com
        "recruiter_email": "recruiter1@test.com",
        "recruiter_name": "Alice Johnson",
        "company_name": "NeuralStack AI",
        "title": "Machine Learning Engineer",
        "department": "AI Research",
        "location": "San Francisco, CA",
        "workArrangement": "Hybrid",
        "type": "Full-time",
        "experienceLevel": "Mid-Level",
        "salary": "$130,000 – $160,000",
        "companyOverview": (
            "NeuralStack AI is a Series-B startup building next-generation "
            "large-language-model infrastructure. Our platform is used by "
            "Fortune 500 companies to fine-tune and deploy custom LLMs at scale."
        ),
        "jobSummary": (
            "We are looking for a skilled Machine Learning Engineer to design, "
            "train, evaluate, and productionise ML models. You will work closely "
            "with research scientists and MLOps engineers to move cutting-edge "
            "research prototypes into low-latency production inference services."
        ),
        "keyResponsibilities": (
            "• Design and implement scalable ML training pipelines using PyTorch and Hugging Face Transformers.\n"
            "• Fine-tune large language models (LLMs) for domain-specific NLP tasks.\n"
            "• Collaborate with data engineers to build feature stores and curate training datasets.\n"
            "• Evaluate model performance using rigorous offline and online metrics.\n"
            "• Deploy models to Kubernetes clusters and monitor production health.\n"
            "• Publish internal technical reports and present at team knowledge-share sessions."
        ),
        "requiredSkills": (
            "Python, PyTorch, TensorFlow, Hugging Face Transformers, scikit-learn, "
            "CUDA, Docker, Kubernetes, MLflow, SQL, Git"
        ),
        "softSkills": "Analytical thinking, strong written communication, team collaboration",
        "educationalBackground": "B.S./M.S. in Computer Science, Statistics, or a related field",
        "preferredQualifications": (
            "Experience with RLHF / DPO fine-tuning; "
            "publications at NeurIPS, ICML, ICLR or similar venues; "
            "familiarity with vLLM or TensorRT-LLM inference stacks."
        ),
        "applicationDeadline": "2025-05-31",
        "requiredDocumentsList": ["Resume", "Cover Letter", "GitHub Profile Link"],
    },
    {
        # recruiter2@test.com
        "recruiter_email": "recruiter2@test.com",
        "recruiter_name": "Bob Martinez",
        "company_name": "CloudForge Systems",
        "title": "Senior DevOps / Platform Engineer",
        "department": "Infrastructure",
        "location": "Austin, TX",
        "workArrangement": "Remote",
        "type": "Full-time",
        "experienceLevel": "Senior",
        "salary": "$140,000 – $175,000",
        "companyOverview": (
            "CloudForge Systems delivers cloud-native platform solutions that "
            "power millions of API requests per day for SaaS companies worldwide. "
            "We believe developer experience is as important as uptime."
        ),
        "jobSummary": (
            "We need a hands-on Senior DevOps / Platform Engineer to evolve our "
            "internal developer platform, improve CI/CD velocity, and reduce "
            "mean-time-to-recovery across our distributed microservices."
        ),
        "keyResponsibilities": (
            "• Architect and maintain multi-cloud infrastructure on AWS and GCP using Terraform.\n"
            "• Design and operate GitOps-based deployment pipelines with ArgoCD and GitHub Actions.\n"
            "• Build internal platform tooling (CLIs, SDKs, developer portals) for 150+ engineers.\n"
            "• Lead SRE practices: SLOs, SLIs, error budgets, incident retrospectives.\n"
            "• Harden Kubernetes clusters and implement zero-trust network policies.\n"
            "• Mentor junior engineers on infra best-practices and cloud security."
        ),
        "requiredSkills": (
            "Terraform, Kubernetes, Helm, ArgoCD, GitHub Actions, AWS, GCP, "
            "Python, Bash, Prometheus, Grafana, Datadog, PostgreSQL, Redis"
        ),
        "softSkills": "Ownership mindset, clear documentation, cross-team communication",
        "educationalBackground": "B.S. in Computer Science, Software Engineering, or equivalent experience",
        "preferredQualifications": (
            "CKA/CKAD certification; experience with Platform Engineering / IDP initiatives; "
            "prior SRE role at a high-traffic company."
        ),
        "applicationDeadline": "2025-06-15",
        "requiredDocumentsList": ["Resume", "LinkedIn Profile", "Infrastructure Portfolio (optional)"],
    },
    {
        # recruiter3@test.com
        "recruiter_email": "recruiter3@test.com",
        "recruiter_name": "Carol Nguyen",
        "company_name": "SecureNet Labs",
        "title": "Cybersecurity Engineer – Threat Detection",
        "department": "Security Operations",
        "location": "Washington, D.C.",
        "workArrangement": "On-site",
        "type": "Full-time",
        "experienceLevel": "Mid-Level",
        "salary": "$120,000 – $150,000",
        "companyOverview": (
            "SecureNet Labs protects critical government and enterprise infrastructure "
            "from sophisticated cyber threats. Our SOC processes over 10 billion security "
            "events daily using proprietary SIEM & AI-driven anomaly detection."
        ),
        "jobSummary": (
            "Join our Threat Detection team to engineer, tune, and operationalise "
            "detection rules and automated response playbooks. You will hunt for advanced "
            "persistent threats (APTs) and contribute to our threat-intelligence pipeline."
        ),
        "keyResponsibilities": (
            "• Develop and continuously refine SIEM detection rules (Splunk SPL, Sigma).\n"
            "• Conduct proactive threat hunting using MITRE ATT&CK TTPs.\n"
            "• Build automated SOAR playbooks to reduce analyst toil.\n"
            "• Perform forensic analysis on endpoints, network captures, and cloud logs.\n"
            "• Collaborate with red team to validate detection coverage.\n"
            "• Produce threat intelligence reports consumed by executive stakeholders."
        ),
        "requiredSkills": (
            "Splunk, Sigma rules, Python, MITRE ATT&CK, Wireshark, Zeek, "
            "SOAR (Palo Alto XSOAR or similar), EDR platforms, Windows & Linux forensics, "
            "TCP/IP networking, SIEM query languages"
        ),
        "softSkills": "Attention to detail, calm under pressure, clear incident reporting",
        "educationalBackground": "B.S. in Computer Science, Information Security, or Cybersecurity",
        "preferredQualifications": (
            "GCIA, GCIH, or OSCP certification; experience with cloud-native security (AWS GuardDuty, Sentinel); "
            "prior work in government or defence environments."
        ),
        "applicationDeadline": "2025-05-20",
        "requiredDocumentsList": ["Resume", "Cover Letter", "Security Clearance (preferred)"],
    },
    {
        # recruiter4@test.com
        "recruiter_email": "recruiter4@test.com",
        "recruiter_name": "David Kim",
        "company_name": "PixelFlow Technologies",
        "title": "Full-Stack Software Engineer (React + Node.js)",
        "department": "Product Engineering",
        "location": "New York, NY",
        "workArrangement": "Hybrid",
        "type": "Full-time",
        "experienceLevel": "Mid-Level",
        "salary": "$110,000 – $140,000",
        "companyOverview": (
            "PixelFlow Technologies builds a B2B SaaS platform that automates "
            "creative asset production for digital advertising agencies. We serve "
            "2,000+ agencies processing over 500,000 creatives per month."
        ),
        "jobSummary": (
            "We are hiring a Full-Stack Engineer to own features end-to-end: "
            "from React interfaces that delight designers to Node.js microservices "
            "that handle high-throughput media processing pipelines."
        ),
        "keyResponsibilities": (
            "• Build responsive, accessible React/TypeScript UIs with a polished UX.\n"
            "• Implement RESTful and GraphQL APIs in Node.js (Express / Fastify).\n"
            "• Design and optimise PostgreSQL schemas and query performance.\n"
            "• Integrate third-party APIs: cloud storage (S3), CDN (Cloudflare), payment (Stripe).\n"
            "• Write unit, integration, and E2E tests (Jest, Playwright).\n"
            "• Participate in code reviews, maintain high engineering standards."
        ),
        "requiredSkills": (
            "React, TypeScript, Node.js, Express, GraphQL, PostgreSQL, Redis, "
            "AWS S3, Docker, Jest, Playwright, Git, REST APIs"
        ),
        "softSkills": "Product sense, proactive communication, empathy for end-users",
        "educationalBackground": "B.S. in Computer Science or equivalent experience",
        "preferredQualifications": (
            "Experience with real-time features (WebSockets, SSE); "
            "prior startup or product-led growth environment exposure; "
            "familiarity with image/video processing libraries (Sharp, FFmpeg)."
        ),
        "applicationDeadline": "2025-06-01",
        "requiredDocumentsList": ["Resume", "Portfolio / GitHub Link", "Brief Cover Letter"],
    },
    {
        # recruiter5@test.com
        "recruiter_email": "recruiter5@test.com",
        "recruiter_name": "Emma Patel",
        "company_name": "DataBridge Analytics",
        "title": "Data Engineer – Real-Time Pipelines",
        "department": "Data Platform",
        "location": "Seattle, WA",
        "workArrangement": "Remote",
        "type": "Full-time",
        "experienceLevel": "Senior",
        "salary": "$135,000 – $165,000",
        "companyOverview": (
            "DataBridge Analytics provides a cloud-native data lakehouse platform "
            "that unifies streaming and batch analytics for enterprise clients in "
            "retail, finance, and healthcare."
        ),
        "jobSummary": (
            "We are looking for a Senior Data Engineer to design and operate "
            "fault-tolerant, low-latency streaming data pipelines that power "
            "real-time dashboards and ML feature stores for our enterprise customers."
        ),
        "keyResponsibilities": (
            "• Design and implement Apache Kafka / Flink streaming pipelines processing millions of events/sec.\n"
            "• Build reliable batch ETL workflows with Apache Spark and dbt on Databricks.\n"
            "• Model data in a medallion-architecture Delta Lake (Bronze → Silver → Gold).\n"
            "• Ensure data quality through automated pipeline monitoring and alerting.\n"
            "• Collaborate with data scientists to deliver features to the ML feature store (Feast).\n"
            "• Mentor junior data engineers and establish engineering best practices."
        ),
        "requiredSkills": (
            "Apache Kafka, Apache Flink, Apache Spark, dbt, Python, Scala, "
            "Delta Lake, Databricks, AWS (S3, Glue, EMR), Airflow, SQL, "
            "Terraform, Docker"
        ),
        "softSkills": "Systems thinking, thoroughness, cross-functional collaboration",
        "educationalBackground": "B.S./M.S. in Computer Science, Data Engineering, or related field",
        "preferredQualifications": (
            "Experience with Iceberg or Hudi table formats; "
            "Kafka certification or Confluent Platform expertise; "
            "background in real-time ML feature engineering."
        ),
        "applicationDeadline": "2025-06-30",
        "requiredDocumentsList": ["Resume", "GitHub / Portfolio Link", "Cover Letter"],
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def signup_recruiter(email: str, name: str, password: str = "Test@1234") -> bool:
    """Register a recruiter account. Returns True on success or if already exists."""
    url = f"{BASE_URL}/api/signup"
    payload = {
        "email": email,
        "password": password,
        "role": "recruiter",
        "name": name,
    }
    try:
        resp = requests.post(url, json=payload, timeout=15)
        data = resp.json()
        if data.get("status") == "success":
            print(f"  [OK]  Registered: {email}")
            return True
        elif "already exists" in data.get("message", "").lower():
            print(f"  [INFO] Already exists: {email} (skipping signup)")
            return True
        else:
            print(f"  [ERROR] Signup failed for {email}: {data.get('message')}")
            return False
    except requests.exceptions.ConnectionError:
        print(
            "\n[ERROR] Could not connect to the backend."
            f"\n        Make sure the Flask server is running at {BASE_URL}"
            "\n        Run: python app.py   (inside the backend directory)"
        )
        sys.exit(1)


def post_job(job_def: dict) -> bool:
    """POST a single job. Returns True on success."""
    url = f"{BASE_URL}/api/jobs"
    payload = {k: v for k, v in job_def.items()
               if k not in ("recruiter_name", "company_name")}
    payload["company"] = job_def["company_name"]

    try:
        resp = requests.post(url, json=payload, timeout=15)
        data = resp.json()
        if data.get("status") == "success":
            job_id = data.get("job", {}).get("id", "unknown")
            print(f"  [OK]  Job posted  id={job_id}  [{job_def['title']}]")
            return True
        else:
            print(f"  [ERROR] Job post failed: {data.get('message')}")
            return False
    except Exception as exc:
        print(f"  [ERROR] Exception posting job: {exc}")
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("  HireAI – Job Seeding Script")
    print(f"  Target: {BASE_URL}")
    print("=" * 60)

    success_count = 0

    for idx, job in enumerate(JOBS, start=1):
        email = job["recruiter_email"]
        name = job["recruiter_name"]
        title = job["title"]

        print(f"\n[{idx}/5] Recruiter: {email}")
        print(f"        Job Title: {title}")

        # Step 1 – ensure recruiter account exists
        if not signup_recruiter(email, name):
            print("       [WARN] Skipping job post due to signup failure.")
            continue

        # Step 2 – post the job
        if post_job(job):
            success_count += 1

    print("\n" + "=" * 60)
    print(f"  Done! {success_count}/{len(JOBS)} jobs posted successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()
