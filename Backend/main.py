from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from routes import transactions, tax, register, login
from sqlalchemy.orm import Session
from models import User
from database import get_db
from passlib.context import CryptContext
from schemas import  UserProfileUpdateSchema,ProfileSchema
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError

app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⛔️ Allows all origins — for development only!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ✅ Include routers
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(tax.router, prefix="/tax", tags=["Tax"])
app.include_router(register.router, prefix="/auth", tags=["Registration"])
app.include_router(login.router, prefix="/auth", tags=["Login"])  # ✅ Added login router

# ✅ Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔐 Secret key and algorithm for JWT
SECRET_KEY = "your_secret_key_here"  # Replace with a strong secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time in minutes


# ✅ Hash password before saving
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# ✅ Verify hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ✅ Create JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ✅ Test route
@app.get("/")
def read_root():
    return {"message": "🚀 Server is working!"}


# ✅ Fetch user profile
@app.get("/profile")
def get_profile(user_email: str = Query(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="❌ User not found")

    return {"username": user.username, "email": user.email}


# ✅ Update user profile
@app.put("/profile/update")
def update_profile(
    user_email: str = Query(...),
    user_data: UserProfileUpdateSchema = None,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="❌ User not found")

    # Update username and password if provided
    if user_data.username:
        user.username = user_data.username
    if user_data.password:
        user.password = hash_password(user_data.password)

    db.commit()
    db.refresh(user)
    return {"message": "✅ Profile updated successfully!"}


if __name__ == "__main__":
    import uvicorn

    print("🚀 Starting FastAPI app...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
