import os
from pypdf import PdfReader
from docx import Document
import io

def extract_text(file_stream, filename):
    """
    Extract text content from various file formats.
    """
    ext = os.path.splitext(filename)[1].lower()
    
    try:
        # pypdf / PdfReader works with file-like objects (bytesio)
        if ext == '.pdf':
            reader = PdfReader(file_stream)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
            
        elif ext in ['.docx', '.doc']:
            doc = Document(file_stream)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
            
        else:
            # Try as raw text
            return file_stream.read().decode('utf-8', errors='ignore')
            
    except Exception as e:
        print(f"Error extracting text from {filename}: {e}")
        return f"[Error: Could not parse {filename}]"
