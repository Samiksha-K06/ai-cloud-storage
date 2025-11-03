# routes/file_routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from database import db
import shutil
import os

# ✅ Define router FIRST
router = APIRouter(
    prefix="/files",
    tags=["Files"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- Upload File ---
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        db.files.insert_one({
            "filename": file.filename,
            "content_type": file.content_type
        })

        return {"message": f"✅ File '{file.filename}' uploaded successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- List Files ---
@router.get("/list")
def list_files():
    files = list(db.files.find({}, {"_id": 0}))
    return {"files": files}

# --- Download File ---
@router.get("/download/{filename}")
def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)

# --- Delete File ---
@router.delete("/delete/{filename}")
def delete_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        db.files.delete_one({"filename": filename})
        return {"message": f"🗑️ File '{filename}' deleted successfully!"}
    else:
        raise HTTPException(status_code=404, detail="File not found")
