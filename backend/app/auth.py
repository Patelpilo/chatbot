from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import users_collection
from passlib.context import CryptContext
import jwt
import datetime

router = APIRouter()

SECRET_KEY = "77e6c32f1aabba124ceb9c36a555cd1f97fe463b14dea97eb311f6c7601304f9"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")



class User(BaseModel):
    email: str
    password: str


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def create_token(email: str):
    payload = {
        "sub": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register")
def register(user: User):
    result = users_collection.insert_one({
        "email": user.email,
        "password": hash_password(user.password)
    })
    print("INSERTED INTO DB:", users_collection.database.name)
    print("COLLECTION:", users_collection.name)
    print("ID:", result.inserted_id)
    return {"message": "User registered successfully"}



@router.post("/login")
def login(user: User):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_token(user.email)
    return {"access_token": token, "token_type": "bearer"}
