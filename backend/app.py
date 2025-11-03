# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import user_routes, file_routes, ai_routes
from dotenv import load_dotenv
import google.generativeai as genai
import os

# --- Load Environment Variables ---
load_dotenv()

# ✅ Configure Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ Missing GEMINI_API_KEY in .env file")
genai.configure(api_key=GEMINI_API_KEY)

# --- Initialize FastAPI app ---
app = FastAPI(
    title="AI Cloud Storage API (Gemini)",
    description="Personal Cloud Storage with AI (Gemini) Organization",
    version="1.0.0"
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Add your frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROUTE IMPORTS ---
app.include_router(user_routes.router)
app.include_router(file_routes.router)
app.include_router(ai_routes.router)

# --- Default Route ---
@app.get("/")
def home():
    return {"message": "✅ AI Cloud Storage Backend (Gemini) is Running!"}
