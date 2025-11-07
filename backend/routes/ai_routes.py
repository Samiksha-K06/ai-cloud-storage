# routes/ai_routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from dotenv import load_dotenv
import google.generativeai as genai
import os
import fitz  # PyMuPDF
import docx

# Load .env variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

router = APIRouter(prefix="/ai", tags=["AI"])

# ✅ Use stable working model from your list
MODEL = "models/gemini-2.5-flash"

def extract_text(file: UploadFile):
    """Extract text from PDF, DOCX, or TXT."""
    try:
        if file.filename.endswith(".pdf"):
            doc = fitz.open(stream=file.file.read(), filetype="pdf")
            text = " ".join(page.get_text("text") for page in doc)
        elif file.filename.endswith(".docx"):
            doc = docx.Document(file.file)
            text = " ".join(p.text for p in doc.paragraphs)
        elif file.filename.endswith(".txt"):
            text = file.file.read().decode("utf-8")
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text extraction failed: {str(e)}")

@router.post("/analyze_file")
async def analyze_file(file: UploadFile = File(...)):
    """Summarize the uploaded document using Gemini."""
    try:
        text = extract_text(file)
        if not text:
            raise HTTPException(status_code=400, detail="No readable text found in file.")

        model = genai.GenerativeModel(MODEL)
        prompt = f"Summarize this document concisely for a quick overview:\n{text[:8000]}"
        response = model.generate_content(prompt)

        summary = response.text.strip() if hasattr(response, "text") else "No summary generated."
        return {"summary": summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
