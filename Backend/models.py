from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP
from database import Base

print("📦 Loading Transaction and User models...")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    transaction_type = Column(String(10), nullable=False)
    crypto_name = Column(String(50), nullable=False)
    quantity = Column(Numeric(18, 8), nullable=False)
    price = Column(Numeric(18, 2), nullable=False)
    transaction_date = Column(TIMESTAMP, nullable=False)
    profit = Column(Numeric(18, 2), nullable=True)



print("✅ Models loaded successfully!")
