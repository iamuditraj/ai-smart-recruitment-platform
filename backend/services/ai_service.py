import os
import google.generativeai as genai

model = None

def init_ai():
    global model
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        print("✅ Gemini AI initialized!")
    else:
        print("⚠️  Warning: GEMINI_API_KEY not found in .env.")

def get_model():
    return model
