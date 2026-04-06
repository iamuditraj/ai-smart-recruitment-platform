import io
import datetime

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
