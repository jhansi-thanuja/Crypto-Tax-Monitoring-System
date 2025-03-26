from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Blessy%**2005@localhost:5433/crypto_tax"  # Replace with your DB URL

print("🔗 Connecting to Database...")
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
    with engine.connect() as conn:
        print("✅ Database connected successfully!")
except Exception as e:
    print(f"❌ Database connection failed: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    print("🗂️ Creating DB session...")
    db = SessionLocal()
    try:
        yield db
    finally:
        print("🔒 Closing DB session...")
        db.close()
