from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from bson import ObjectId
from database import db
from passlib.context import CryptContext
from jose import JWTError, jwt
import datetime
import os

router = APIRouter(prefix="/users", tags=["Users"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Secret Key
SECRET_KEY = "mysecretkey"  # you can store in .env later
ALGORITHM = "HS256"

# Pydantic Models
class User(BaseModel):
    username: str
    email: str
    password: str

# Signup Route
@router.post("/signup")
def signup(user: User):
    existing_user = db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = pwd_context.hash(user.password)
    db.users.insert_one({
        "username": user.username,
        "email": user.email,
        "password": hashed_password
    })
    return {"message": "✅ User registered successfully!"}

# Login Route
class LoginModel(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(user: LoginModel):
    db_user = db.users.find_one({"email": user.email})
    if not db_user or not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token_data = {
        "sub": str(db_user["_id"]),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
