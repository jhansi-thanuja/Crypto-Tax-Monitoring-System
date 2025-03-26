from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import User
from schemas import UserLoginSchema
from database import get_db
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

router = APIRouter()

# JWT Secret and Algorithm
SECRET_KEY = "mysecretkey123"
ALGORITHM = "HS256"

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ✅ Verify hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# ✅ Create JWT token with email and user_id
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login")
def login(user_data: UserLoginSchema, db: Session = Depends(get_db)):
    # ✅ Fetch user by email
    user = db.query(User).filter(User.email == user_data.email).first()

    # ❌ Invalid email or password
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")


    # ✅ Generate JWT token with email and user_id
    token_data = {"sub": user.email, "user_id": user.id}
    token = create_access_token(token_data)

    # ✅ Return token and user_id
    return {
        "message": "✅ Login successful!",
        "token": token,
        "user_id": user.id,
    }
