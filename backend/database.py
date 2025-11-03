from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi   # 👈 important for SSL fix

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

try:
    # Connect to MongoDB Atlas securely
    client = MongoClient(MONGO_URI, tls=True, tlsCAFile=certifi.where())
    db = client["ai_cloud_storage"]
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print("❌ MongoDB connection failed:", e)
