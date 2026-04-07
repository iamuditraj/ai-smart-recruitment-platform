import io
import datetime
from firebase_admin import firestore

def get_user_collection(db, email: str):
    """
    Looks up user_index collection, returns tuple of (role, collection_name).
    Used to avoid repeating this pattern in routes.
    """
    index_doc = db.collection('user_index').document(email).get()
    user_role = index_doc.to_dict().get('role') if index_doc.exists else None
    collection_name = 'recruiters' if user_role == 'recruiter' else 'candidates'
    return user_role, collection_name

def serialize_timestamps(doc_dict: dict) -> dict:
    """
    Converts any Firestore DatetimeWithNanoseconds fields (or similar datetime objects)
    to ISO strings. Returns the modified dict.
    """
    if not isinstance(doc_dict, dict):
        return doc_dict
    
    for key, val in doc_dict.items():
        if val and hasattr(val, 'isoformat') and callable(val.isoformat):
            # Convert timezone aware firestore datetime to isoformat
            try:
                doc_dict[key] = val.isoformat()
            except Exception:
                pass
    return doc_dict

def build_ats_pipeline(resume_file, jd_text: str, parsed_jd: dict):
    """
    Takes a file stream + jd text + parsed jd dict, 
    runs extract_text -> parse_resume_against_jd -> score_resume, 
    returns (ats_result, llm_parsed_resume).
    """
    from services.ai_service import parse_resume_against_jd
    from services.parser_service import extract_text
    from services.ats.scorer import score_resume
    
    file_stream = io.BytesIO(resume_file.read())
    # Note: resume_file can be used like request.files['resume'] which has a filename attribute.
    extracted_resume_text = extract_text(file_stream, getattr(resume_file, 'filename', 'resume.pdf'))
    llm_parsed_resume = parse_resume_against_jd(extracted_resume_text, jd_text)
    ats_result = score_resume(llm_parsed_resume, parsed_jd, extracted_resume_text)
    
    return ats_result, llm_parsed_resume


def save_resume_to_profile(db, email, resume_id, resume_doc, parent_extras=None):
    """
    Save a resume document to ``candidates/{email}/resumes/{resume_id}``.

    Automatically checks if this is the candidate's first resume and marks
    it as the default.  When it *is* the default, the parent candidate
    document is updated with ``defaultResumeId`` plus any additional fields
    supplied in *parent_extras*.

    Returns True if the saved resume became the default.
    """
    candidate_ref = db.collection('candidates').document(email)

    is_default = len(list(candidate_ref.collection('resumes').stream())) == 0
    resume_doc['isDefault'] = is_default
    resume_doc['uploadedAt'] = datetime.datetime.utcnow().isoformat()

    candidate_ref.collection('resumes').document(resume_id).set(resume_doc)

    if is_default:
        update_data = {
            'defaultResumeId': resume_id,
            'updatedAt': firestore.SERVER_TIMESTAMP,
        }
        if parent_extras:
            update_data.update(parent_extras)
        candidate_ref.update(update_data)

    return is_default


def build_jd_from_job(job_data: dict) -> tuple:
    """Build full JD text from a Firestore job document and parse it with Groq.

    Returns ``(jd_text, parsed_jd)`` where *parsed_jd* is the LLM-structured dict.
    """
    from services.ai_service import parse_job_description

    parts = []
    for field in ['title', 'jobSummary', 'description', 'keyResponsibilities',
                  'requiredSkills', 'softSkills', 'preferredQualifications',
                  'educationalBackground', 'experienceLevel', 'companyOverview']:
        val = job_data.get(field, '')
        if val:
            parts.append(f"{field}: {val}")
    jd_text = "\n".join(parts)

    parsed_jd = parse_job_description(jd_text)
    return jd_text, parsed_jd


def get_job_with_parsed_jd(db, job_id):
    """Fetch a job document and parse its JD in one step.

    Returns ``(job_data, jd_text, parsed_jd)``.
    Returns ``(None, None, None)`` if the job does not exist.
    """
    job_doc = db.collection('jobs').document(job_id).get()
    if not job_doc.exists:
        return None, None, None
    job_data = job_doc.to_dict()
    jd_text, parsed_jd = build_jd_from_job(job_data)
    return job_data, jd_text, parsed_jd


def enrich_app_with_candidate(db, app_data):
    """Enrich an application dict with data from the candidate's profile.

    Adds ``candidate_name``, ``resumeUrl``, ``resumeName``, ``experience``,
    and ``parsedResume`` (if not already present) from the candidate document.
    Mutates *app_data* in place and returns it.
    """
    c_email = app_data.get('candidate_email')
    if not c_email:
        return app_data

    user_doc = db.collection('candidates').document(c_email).get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        app_data['candidate_name'] = user_data.get('name', c_email.split('@')[0])
        if not app_data.get('parsedResume'):
            app_data['parsedResume'] = user_data.get('parsedResume')
        app_data.setdefault('resumeUrl', user_data.get('resumeUrl'))
        app_data.setdefault('resumeName', user_data.get('resumeName'))
        app_data.setdefault('experience', user_data.get('bio', ''))
    else:
        if not app_data.get('candidate_name'):
            app_data['candidate_name'] = c_email.split('@')[0]

    return app_data
