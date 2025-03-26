from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserResponse
from database import get_db
from passlib.context import CryptContext

router = APIRouter()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hash password before saving
def hash_password(password):
    return pwd_context.hash(password)


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists.")
    
    # Hash the password
    hashed_password = hash_password(user.password)

    # Create a new user
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # ✅ Updated response with user data
    return {
        "message": "User registered successfully!",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
        },
    }
