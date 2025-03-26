from sqlalchemy.orm import Session
from models import Transaction
from schemas import TransactionCreate

# Create a new transaction
def create_transaction(db: Session, transaction: TransactionCreate):
    db_transaction = Transaction(
        user_id=transaction.user_id,
        transaction_type=transaction.transaction_type,
        crypto_name=transaction.crypto_name,
        quantity=transaction.quantity,
        price=transaction.price,
        transaction_date=transaction.transaction_date,
        profit=transaction.profit
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# Get transaction by ID
def get_transaction(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()

# Get all transactions
def get_transactions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Transaction).offset(skip).limit(limit).all()

# Update a transaction
def update_transaction(db: Session, transaction_id: int, updated_data: dict):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if db_transaction:
        for key, value in updated_data.items():
            setattr(db_transaction, key, value)
        db.commit()
        db.refresh(db_transaction)
    return db_transaction

# Delete a transaction
def delete_transaction(db: Session, transaction_id: int):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
    return db_transaction
