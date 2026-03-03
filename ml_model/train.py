import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import spacy

# Load NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    doc = nlp(text.lower())
    # Remove stopwords and punctuation, keep only lemmas
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

def train_ranking_model(train_data_path, model_output_path):
    print(f"Loading training data from {train_data_path}...")
    
    # Placeholder: In a real scenario, you'd iterate through PDF/Docx files
    # For now, we'll assume a CSV structure or simple text files
    # Let's create dummy content if the folder is empty
    resumes = []
    labels = [] # Job categories or relevance scores
    
    # Load resumes
    valid_extensions = ('.txt', '.pdf', '.docx')
    resume_files = [f for f in os.listdir(train_data_path) if f.lower().endswith(valid_extensions)]
    
    if not resume_files:
        print("No valid resume files found in training directory. Using fallback sample data...")
        sample_data = [
            ("Experienced Python Developer with expertise in Flask and Django", "Software Engineer"),
            ("Data Scientist with PhD in statistics and deep learning experience", "Data Science"),
            ("Senior HR Manager specializing in tech recruitment and talent acquisition", "HR"),
            ("Frontend Developer proficient in React, Vue and modern CSS", "Frontend Engineer"),
            ("DevOps Engineer with Kubernetes and AWS certification", "DevOps")
        ]
        resumes = [preprocess_text(r[0]) for r in sample_data]
    else:
        print(f"Loading {len(resume_files)} resumes from {train_data_path}...")
        for f in resume_files:
            file_path = os.path.join(train_data_path, f)
            # Basic text reader for now
            if f.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    resumes.append(preprocess_text(content))
            # Placeholder for PDF/DOCX - could use PyPDF2 / docx here
            else:
                print(f"Skipping {f} (Advanced parsing for PDF/DOCX can be added later)")

    if not resumes:
        print("Error: No resumes to train on.")
        return

    print(f"Vectorizing {len(resumes)} resumes...")
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(resumes)
    
    # Save model artifacts
    print(f"Saving artifacts to {model_output_path}...")
    if not os.path.exists(model_output_path):
        os.makedirs(model_output_path)
        
    joblib.dump(vectorizer, os.path.join(model_output_path, "vectorizer.pkl"))
    joblib.dump(tfidf_matrix, os.path.join(model_output_path, "resume_vectors.pkl"))
    
    print("Training complete!")

if __name__ == "__main__":
    # Get the directory where the script is located
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TRAIN_DIR = os.path.join(BASE_DIR, "datasets", "train")
    MODEL_DIR = os.path.join(BASE_DIR, "models")
    
    # Create directories if they don't exist
    if not os.path.exists(TRAIN_DIR):
        os.makedirs(TRAIN_DIR)
    
    train_ranking_model(TRAIN_DIR, MODEL_DIR)
