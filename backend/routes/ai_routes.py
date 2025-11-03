from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import google.generativeai as genai
from dotenv import load_dotenv
import os
import fitz  # PyMuPDF
import docx
from io import BytesIO

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


# ✅ Helper: Extract text safely from TXT, PDF, DOCX
def extract_text_from_file(file: UploadFile) -> str:
    file_ext = file.filename.split(".")[-1].lower()
    file_bytes = file.file.read()

    if file_ext == "txt":
        return file_bytes.decode("utf-8", errors="ignore")

    elif file_ext == "pdf":
        text = ""
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text

    elif file_ext == "docx":
        doc = docx.Document(BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs)

    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload .txt, .pdf, or .docx."
        )


# 🧠 1️⃣ Basic test route
@router.get("/analyze")
async def analyze_text():
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content("Summarize this file: Sample text content.")
        return {"ai_response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 💬 2️⃣ Analyze raw text directly
@router.post("/analyze_text")
async def analyze_custom_text(text: str = Form(...)):
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(f"Summarize this text:\n{text}")
        return {"summary": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 📄 3️⃣ Analyze uploaded file (TXT / PDF / DOCX)
@router.post("/analyze_file")
async def analyze_file(file: UploadFile = File(...)):
    try:
        text = extract_text_from_file(file)
        if not text.strip():
            raise HTTPException(status_code=400, detail="File appears to be empty.")

        # Limit text to 4000 characters (Gemini context limit safety)
        text_chunk = text[:4000]

        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(f"Summarize this document:\n\n{text_chunk}")


        # ✅ Extract summary safely
        summary = None
        try:
            if hasattr(response, "text") and response.text:
                summary = response.text.strip()
            elif response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                if hasattr(candidate, "content") and hasattr(candidate.content, "parts"):
                    parts = candidate.content.parts
                    summary = "".join([p.text for p in parts if hasattr(p, "text")]).strip()
        except Exception as e:
            print("⚠️ Error extracting summary:", e)
            summary = None

        # 🧩 Fallback
        if not summary or summary.strip() == "":
            summary = f"(Fallback summary) The document '{file.filename}' contains approximately {len(text.split())} words."

        return {
            "filename": file.filename,
            "summary": summary
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
