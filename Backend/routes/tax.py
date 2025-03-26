from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from decimal import Decimal
from models import Transaction
from schemas import TaxResponse
from database import get_db

router = APIRouter()

# ✅ Tax percentages
SHORT_TERM_TAX_RATE = Decimal("0.3")  # 30% for short-term
LONG_TERM_TAX_RATE = Decimal("0.1")  # 10% for long-term
EXEMPTION_LIMIT = Decimal("50000.00")  # Exempt up to 50,000 profit

# ✅ Correct tax calculation logic
def calculate_tax(transaction_details):
    total_profit = Decimal(0)
    short_term_profit = Decimal(0)
    long_term_profit = Decimal(0)

    for tx in transaction_details:
        profit_loss = Decimal(tx["profit_loss"])
        transaction_date = datetime.strptime(tx["transaction_date"], "%Y-%m-%d %H:%M:%S")
        holding_period = (datetime.now() - transaction_date).days

        if profit_loss > 0:
            # ✅ Short-term if holding period < 365 days
            if holding_period < 365:
                short_term_profit += profit_loss
            else:
                long_term_profit += profit_loss

        total_profit += profit_loss

    # ✅ Apply exemption limit
    taxable_profit = total_profit - EXEMPTION_LIMIT if total_profit > EXEMPTION_LIMIT else Decimal(0)

    # ✅ Tax calculation
    short_term_tax = short_term_profit * SHORT_TERM_TAX_RATE
    long_term_tax = long_term_profit * LONG_TERM_TAX_RATE

    total_tax = short_term_tax + long_term_tax

    return float(total_tax) if taxable_profit > 0 else 0.0


# ✅ Get tax summary for user
@router.get("/summary/{user_id}", response_model=TaxResponse)
def get_tax_summary(user_id: int, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()

    if not transactions:
        return {
            "user_id": user_id,
            "total_profit": 0.0,
            "tax_amount": 0.0,
            "transaction_details": [],
        }

    transaction_details = []
    total_profit = Decimal(0)

    for tx in transactions:
        quantity = Decimal(tx.quantity)
        price = Decimal(tx.price)
        amount = quantity * price
        profit_loss = amount if tx.transaction_type == "Sell" else -amount

        transaction_details.append({
            "crypto_name": tx.crypto_name,
            "transaction_type": tx.transaction_type,
            "quantity": float(quantity),
            "price": float(price),
            "amount": float(amount),
            "profit_loss": float(profit_loss),
            "transaction_date": str(tx.transaction_date),
        })
        total_profit += profit_loss

    # ✅ Calculate tax correctly
    tax_amount = calculate_tax(transaction_details)

    return {
        "user_id": user_id,
        "total_profit": float(total_profit),
        "tax_amount": tax_amount,
        "transaction_details": transaction_details,
    }
