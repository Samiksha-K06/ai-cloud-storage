from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import file_routes, ai_routes, user_routes
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize FastAPI
app = FastAPI(
    title="AI Cloud Storage",
    description="Personal Cloud Storage with Gemini AI Integration",
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_routes.router)
app.include_router(file_routes.router)
app.include_router(ai_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to AI Cloud Storage API 🚀"}
