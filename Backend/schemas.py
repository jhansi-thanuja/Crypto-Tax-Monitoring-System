from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Dict

print("📚 Loading schemas...")


# ✅ Transaction Schema
class TransactionSchema(BaseModel):
    transaction_type: str  # "buy" or "sell"
    crypto_name: str
    quantity: float
    price: float
    transaction_date: datetime
    profit: Optional[float] = None

    class Config:
        from_attributes = True


# ✅ Transaction Create Schema
class TransactionCreate(BaseModel):
    transaction_type: str
    crypto_name: str
    quantity: float
    price: float
    transaction_date: datetime
    user_id: int


# ✅ Transaction Update Schema
class TransactionUpdate(BaseModel):
    transaction_type: str
    crypto_name: str
    quantity: float
    price: float
    transaction_date: datetime


# ✅ Transaction Response Schema
class TransactionResponse(BaseModel):
    id: int
    user_id: int
    transaction_type: str
    crypto_name: str
    quantity: float
    price: float
    transaction_date: datetime

    class Config:
        orm_mode = True


# ✅ Tax Response Schema
class TaxResponse(BaseModel):
    user_id: int
    total_tax: float
    tax_breakdown: Dict[str, float]
    generated_at: datetime

    class Config:
        orm_mode = True


# ✅ User Registration Schema
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


# ✅ User Response Schema
class UserData(BaseModel):
    id: int
    username: str


class UserResponse(BaseModel):
    message: str
    user: UserData


# ✅ User Login Schema
class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


# ✅ User Profile Schema for fetching and updating
class ProfileSchema(BaseModel):
    username: str
    email: EmailStr
    password: Optional[str] = None  # Optional password field

    class Config:
        orm_mode = True


# ✅ User Profile Update Schema (Optional fields)
class UserProfileUpdateSchema(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


print("✅ Schemas loaded successfully!")
