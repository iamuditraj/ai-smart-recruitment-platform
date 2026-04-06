from flask import Blueprint, jsonify, request
from services.firebase_service import get_db
from firebase_admin import firestore
import datetime
import json
import io

from services.db_helpers import build_ats_pipeline
from services.ai_service import get_model, MODEL, parse_job_description, parse_resume_against_jd
from services.parser_service import extract_text
from services.ats.scorer import score_resume

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/api/generate-content', methods=['POST'])
def generate_content():
    try:
        data = request.json
        prompt = data.get('prompt')
        context = data.get('context', '')
        
        if not prompt:
            return jsonify({"status": "error", "message": "No prompt provided"}), 400

        full_prompt = f"Context: {context}\n\nTask: {prompt}\n\nPlease generate concise, professional resume content based on the task and context above."
        
        model = get_model()
        if not model:
            return jsonify({"status": "error", "message": "AI model not initialized"}), 500

        response = model.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": full_prompt}],
            temperature=0.7,
        )
        return jsonify({
            "status": "success",
            "content": response.choices[0].message.content
        })
    except Exception as e:
        print(f"Error in generate_content: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@ai_bp.route('/api/generate-assessment', methods=['POST'])
def generate_assessment():
    try:
        model = get_model()
        if not model:
            return jsonify({"status": "error", "message": "AI model not initialized"}), 500

        data = request.json
        role_label = data.get('role', 'Generic Developer')
        
        prompt = f"""
        Generate a professional technical skill assessment for the role: {role_label}.
        
        Requirements:
        1. Create exactly 5 multiple-choice questions.
        2. Questions should range from basic to intermediate difficulty.
        3. Respond ONLY with a JSON array of objects, with this structure:
           [
             {{
               "text": "The question text?",
               "options": ["Option A", "Option B", "Option C", "Option D"],
               "correct": 1  // index of the correct option (0-3)
             }}
           ]
        
        JSON only. No Markdown, no explanations.
        """
        
        response = model.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        raw = json.loads(response.choices[0].message.content)
        questions = raw if isinstance(raw, list) else raw.get("questions", [])
        
        if not questions:
            return jsonify({"status": "error", "message": "Failed to generate AI questions"}), 500
            
        return jsonify({
            "status": "success",
            "questions": questions
        })
    except Exception as e:
        print(f"Error in generate_assessment: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@ai_bp.route('/api/parse-jd', methods=['POST'])
def parse_jd_endpoint():
    try:
        data = request.json
        if not data or 'jd_text' not in data:
            return jsonify({"status": "error", "message": "Missing jd_text"}), 400
        
        parsed_jd = parse_job_description(data['jd_text'])
        return jsonify({
            "status": "success",
            "parsed_jd": parsed_jd
        })
    except Exception as e:
        print(f"Error parsing JD: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@ai_bp.route('/api/score-resume', methods=['POST'])
def score_resume_endpoint():
    try:
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "Invalid payload"}), 400
            
        resume_text = data.get('resume_text')
        raw_jd_text = data.get('raw_jd_text', '')
        parsed_jd = data.get('parsed_jd')
        
        if not resume_text or not parsed_jd:
            return jsonify({"status": "error", "message": "Missing resume_text or parsed_jd"}), 400
            
        llm_parsed_resume = parse_resume_against_jd(resume_text, raw_jd_text)
        ats_result = score_resume(llm_parsed_resume, parsed_jd, resume_text)
        
        return jsonify({
            "status": "success",
            "score": ats_result
        })
    except Exception as e:
        print(f"Error in score-resume: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@ai_bp.route('/api/analyze', methods=['POST'])
def analyze_resumes():
    try:
        job_description = request.form.get('jobDescription', '')
        resumes = request.files.getlist('resumes')

        if not resumes:
            return jsonify({"status": "error", "message": "No resumes uploaded"}), 400

        if not job_description.strip():
            return jsonify({"status": "error", "message": "Job description is required for ATS scoring"}), 400

        parsed_results = []
        parsed_jd = parse_job_description(job_description)

        for file in resumes:
            try:
                ats_result, llm_parsed_resume = build_ats_pipeline(file, job_description, parsed_jd)
                result = ats_result
                result['name'] = file.filename
            except Exception as score_err:
                print(f"ATS scoring error for {file.filename}: {score_err}")
                result = {
                    "name":       file.filename,
                    "score":      0,
                    "status":     "Error",
                    "badgeClass": "badge-danger",
                    "skills":     [],
                    "experience": "Could not parse resume",
                    "category":   "OTHER",
                    "score_breakdown": {},
                    "matched_skills":  [],
                    "key_gaps":        [],
                }

            parsed_results.append(result)

        parsed_results.sort(key=lambda x: x.get('score', 0), reverse=True)

        return jsonify({
            "status":  "success",
            "message": f"Successfully analyzed {len(parsed_results)} resumes!",
            "results": parsed_results,
            "engine":  "local_ats_v1",
        })

    except Exception as e:
        print(f"Error in analyze_resumes: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@ai_bp.route('/api/save-resume', methods=['POST'])
def save_resume():
    try:
        db = get_db()
        if not db:
            return jsonify({"status": "error", "message": "Firebase not initialized"}), 500
            
        data = request.json
        resume_id = data.get('metadata', {}).get('resume_id')
        
        if not resume_id:
            return jsonify({"status": "error", "message": "No resume_id provided"}), 400
            
        email = data.get('profile', {}).get('contact', {}).get('email')
        if email:
            candidate_ref = db.collection('candidates').document(email)
            doc_snap = candidate_ref.get()
            if doc_snap.exists:
                is_default = len(list(candidate_ref.collection('resumes').stream())) == 0
                
                new_resume = {
                    'id': resume_id,
                    'resume_id': resume_id,
                    'type': 'generated',
                    'resumeName': f"Generated Resume - {data.get('profile', {}).get('job_title', 'Role')}",
                    'parsedResume': data,
                    'isDefault': is_default,
                    'uploadedAt': datetime.datetime.utcnow().isoformat()
                }
                
                candidate_ref.collection('resumes').document(resume_id).set(new_resume)
                
                if is_default:
                    update_data = {
                        'defaultResumeId': resume_id,
                        'updatedAt': firestore.SERVER_TIMESTAMP
                    }
                    candidate_ref.update(update_data)
        
        return jsonify({
            "status": "success",
            "message": f"Resume {resume_id} saved successfully to Firestore!"
        })
    except Exception as e:
        print(f"Error in save_resume: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
