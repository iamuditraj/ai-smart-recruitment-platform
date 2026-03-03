import joblib
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import spacy

nlp = spacy.load("en_core_web_sm")

def preprocess(text):
    doc = nlp(text.lower())
    return " ".join([t.lemma_ for t in doc if not t.is_stop and not t.is_punct])

def rank_candidates(job_description, model_dir="models"):
    vectorizer = joblib.load(os.path.join(model_dir, "vectorizer.pkl"))
    resume_vectors = joblib.load(os.path.join(model_dir, "resume_vectors.pkl"))
    
    # Process JD
    processed_jd = preprocess(job_description)
    jd_vector = vectorizer.transform([processed_jd])
    
    # Calculate similarity
    similarities = cosine_similarity(jd_vector, resume_vectors).flatten()
    
    # Sort and rank
    rankings = np.argsort(similarities)[::-1]
    
    print("\n--- AI Candidate Ranking Results ---")
    for i, idx in enumerate(rankings):
        print(f"Rank {i+1}: Candidate {idx} - Score: {similarities[idx]:.4f}")

if __name__ == "__main__":
    # Get the directory where the script is located
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_DIR = os.path.join(BASE_DIR, "models")
    
    test_jd = "Looking for a Python Developer with experience in web frameworks like Flask."
    if os.path.exists(os.path.join(MODEL_DIR, "vectorizer.pkl")):
        rank_candidates(test_jd, MODEL_DIR)
    else:
        print(f"Model artifacts not found in {MODEL_DIR}. Please run train.py first.")
