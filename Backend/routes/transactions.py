from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Transaction
from schemas import TransactionCreate, TransactionResponse, TransactionUpdate
from database import get_db

router = APIRouter()


# ✅ Get all transactions
@router.get("/show", response_model=list[TransactionResponse])
def get_transactions(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    return transactions


# ✅ Get transactions by user_id
@router.get("/show/{user_id}", response_model=list[TransactionResponse])
def get_transactions_by_user(user_id: int, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found for this user.")
    return transactions


# ✅ Create a new transaction
@router.post("/create-transaction", response_model=TransactionResponse)
async def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    try:
        new_transaction = Transaction(
            user_id=transaction.user_id,
            transaction_type=transaction.transaction_type,
            crypto_name=transaction.crypto_name,
            quantity=transaction.quantity,
            price=transaction.price,
            transaction_date=transaction.transaction_date,
        )
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
        return new_transaction
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating transaction: {str(e)}")


# ✅ Update transaction by user_id and transaction_id
@router.put("/update/{user_id}/{id}", response_model=TransactionResponse)
async def update_transaction(
    user_id: int, id: int, transaction: TransactionUpdate, db: Session = Depends(get_db)
):
    existing_transaction = (
        db.query(Transaction)
        .filter(Transaction.id == id, Transaction.user_id == user_id)
        .first()
    )
    if not existing_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Update transaction fields
    existing_transaction.transaction_type = transaction.transaction_type
    existing_transaction.crypto_name = transaction.crypto_name
    existing_transaction.quantity = transaction.quantity
    existing_transaction.price = transaction.price
    existing_transaction.transaction_date = transaction.transaction_date

    db.commit()
    db.refresh(existing_transaction)
    return existing_transaction


# ✅ Delete transaction
@router.delete("/delete/{user_id}/{id}")
async def delete_transaction(user_id: int, id: int, db: Session = Depends(get_db)):
    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == id, Transaction.user_id == user_id)
        .first()
    )
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}
