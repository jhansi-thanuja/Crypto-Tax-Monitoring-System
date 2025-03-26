from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from schemas import ProfileSchema
from database import get_db
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password before updating
def hash_password(password):
    return pwd_context.hash(password)

# Get Profile Data (Include id, username, and email)
# Get Profile Data
@router.get("/profile")
def get_profile(user_email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Return id, username, and email
    return {"id": user.id, "username": user.username, "email": user.email}

# Update Profile (Allow changing username and password)
@router.put("/profile/update")
def update_profile(
    user_email: str, profile_data: ProfileSchema, db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update username and email
    user.username = profile_data.username
    user.email = profile_data.email

    # Update password only if provided
    if profile_data.password:
        user.password = hash_password(profile_data.password)

    db.commit()
    db.refresh(user)
    return {"message": "Profile updated successfully"}
