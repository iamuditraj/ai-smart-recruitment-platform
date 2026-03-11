import spacy
import re
import json
import sys
from pypdf import PdfReader

# Load spaCy model once at module level (slow to load, so do it only once)
nlp = spacy.load("en_core_web_sm")

SKILLS_LIST = [
    "python", "java", "javascript", "react", "node.js",
    "sql", "machine learning", "deep learning", "data analysis",
    "communication", "leadership", "teamwork"
    # add more as needed
]

# ── PDF Reader ────────────────────────────────────────────────────────────────

def extract_text_from_pdf(pdf_path):
    """Read a PDF file and return all its text as a single string."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# ── Field Extractors ──────────────────────────────────────────────────────────

def extract_labeled_field(text, *labels):
    """Extract value from a labeled line like 'Name: John Doe'"""
    for label in labels:
        match = re.search(rf'{label}\s*[:\-]\s*(.+)', text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None

def extract_email(text):
    match = re.findall(r'[\w.-]+@[\w.-]+\.\w+', text)
    return match[0] if match else None

def extract_phone(text):
    match = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text)
    return match[0] if match else None

def extract_skills(text):
    # First try label-based: "Skills: Python, SQL, ..."
    labeled = extract_labeled_field(text, "skills", "skill")
    if labeled:
        found = [s.strip().lower() for s in labeled.split(",") if s.strip().lower() in SKILLS_LIST]
        if found:
            return found

    # Fallback: scan full text
    text_lower = text.lower()
    return [skill for skill in SKILLS_LIST if skill in text_lower]

def extract_experience(text):
    return extract_labeled_field(text, "experience", "exp")

# ── Main Parser ───────────────────────────────────────────────────────────────

def extract_name_fallback(text):
    """Use the first clean line as the name (most resumes put name at top)."""
    for line in text.strip().splitlines():
        line = line.strip()
        # Skip blank lines, lines with email/phone/digits/special chars
        if line and not re.search(r'[@\d|:/\\]', line) and len(line.split()) <= 5:
            return line
    return None

def parse_resume(text):
    """Parse raw resume text and return structured data."""
    # Name: try label first, then first-line fallback
    name = extract_labeled_field(text, "name") or extract_name_fallback(text)

    # Experience: try label first, then look for year/duration pattern
    experience = extract_experience(text)
    if not experience:
        match = re.search(r'(\d+\+?\s*years?[^\n]{0,60})', text, re.IGNORECASE)
        if match:
            experience = match.group(1).strip()

    return {
        "name":       name,
        "phone":      extract_labeled_field(text, "phone", "mobile", "contact") or extract_phone(text),
        "email":      extract_email(text),
        "skills":     extract_skills(text),
        "experience": experience,
    }

def parse_resume_from_pdf(pdf_path):
    """Extract text from a PDF file and parse it."""
    print(f"Reading PDF: {pdf_path}")
    text = extract_text_from_pdf(pdf_path)
    return parse_resume(text)

# ── Test Block ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # If a PDF path is passed as argument: python preprocess.py resume.pdf
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        result = parse_resume_from_pdf(pdf_path)
    else:
        # Default: test with sample text
        sample = """
        Name: Jon Doe
        Phone: +91 9876543210
        Email: Jondoe@email.com
        Skills: Python, Machine Learning, SQL, Communication
        Experience: 3 years at ABC Corp as Data Analyst
        """
        result = parse_resume(sample)

    print(json.dumps(result, indent=2))
