from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from database import db
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import os
import uuid

router = APIRouter(prefix="/files", tags=["Files"])

load_dotenv()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # ✅ Upload file to Cloudinary
        result = cloudinary.uploader.upload(file.file, resource_type="auto")

        # ✅ Save file info to MongoDB
        file_data = {
            "filename": file.filename,
            "url": result["secure_url"],
            "public_id": result["public_id"]
        }

        inserted = db["files"].insert_one(file_data)

        # ✅ Convert ObjectId to string before returning
        return JSONResponse({
            "message": "File uploaded successfully",
            "file_id": str(inserted.inserted_id),
            "file_url": result["secure_url"]
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ File List
@router.get("/list")
async def list_files():
    try:
        files = list(db.files.find({}, {"_id": 0}))
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Delete File
@router.delete("/delete/{public_id}")
async def delete_file(public_id: str):
    try:
        # Get file type from DB
        file_record = db.files.find_one({"public_id": public_id})
        if not file_record:
            raise HTTPException(status_code=404, detail="File not found")

        resource_type = file_record.get("resource_type", "raw")

        cloudinary.uploader.destroy(public_id, resource_type=resource_type)
        db.files.delete_one({"public_id": public_id})

        return {"message": "🗑️ File deleted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
