# ML Resume Ranking Model

This directory contains the machine learning logic for ranking resumes based on job descriptions using Natural Language Processing (NLP).

## Structure

- `datasets/train/`: Place resumes (PDF/DOCX/TXT) used for building the initial vocabulary and vector space.
- `datasets/test/`: Place resumes for evaluation and testing.
- `notebooks/`: Jupyter notebooks for data exploration and model prototyping.
- `src/`: Reusable Python modules for text parsing, cleaning, and feature engineering.
- `train.py`: Main script to preprocess training data and save model artifacts (vectorizers, embeddings).
- `evaluate.py`: Script to test the ranking logic against sample Job Descriptions.

## How to Get Started

1. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Add Data**:
   Place resume files in `datasets/train/`.

3. **Train**:

   ```bash
   python train.py
   ```

   This will generate a `models/` directory containing the saved artifacts.

4. **Evaluate**:
   ```bash
   python evaluate.py
   ```

## NLP Pipeline

- **Text Extraction**: Converting documents to plain text.
- **Preprocessing**: Lemmatization, stop-word removal, and normalization using `spaCy`.
- **Vectorization**: Representing text as numeric vectors (currently using TF-IDF, can be upgraded to Word2Vec or BERT).
- **Ranking**: Calculating Cosine Similarity between the Job Description vector and Resume vectors.
