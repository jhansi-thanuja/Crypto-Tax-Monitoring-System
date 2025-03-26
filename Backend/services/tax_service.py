from sqlalchemy.orm import Session
from models import Transaction
from schemas import TaxResponse
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

def calculate_tax(user_id: int, db: Session) -> TaxResponse:
    print(f"📊 Fetching transactions for user_id: {user_id}")
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()

    total_profit = Decimal(0)
    buy_transactions = {}

    # Process all transactions to store buy prices
    for txn in transactions:
        if txn.transaction_type == "buy":
            if txn.crypto_name not in buy_transactions:
                buy_transactions[txn.crypto_name] = []
            buy_transactions[txn.crypto_name].append(txn)

    # Match with sell transactions and calculate profit
    for txn in transactions:
        if txn.transaction_type == "sell":
            if txn.crypto_name in buy_transactions and buy_transactions[txn.crypto_name]:
                remaining_quantity = Decimal(txn.quantity)
                profit = Decimal(0)

                # Process each buy txn until the full sell quantity is matched
                while remaining_quantity > 0 and buy_transactions[txn.crypto_name]:
                    buy_txn = buy_transactions[txn.crypto_name].pop(0)
                    buy_price = Decimal(buy_txn.price)
                    buy_qty = Decimal(buy_txn.quantity)

                    # If buy quantity is more than the sell quantity, adjust the buy transaction
                    if buy_qty > remaining_quantity:
                        profit += (Decimal(txn.price) - buy_price) * remaining_quantity
                        # Update the remaining quantity of the buy transaction
                        buy_txn.quantity = str(buy_qty - remaining_quantity)
                        buy_transactions[txn.crypto_name].insert(0, buy_txn)
                        break
                    else:
                        profit += (Decimal(txn.price) - buy_price) * buy_qty
                        remaining_quantity -= buy_qty
                total_profit += profit
            else:
                logger.warning(f"No buy transaction found for sell of {txn.crypto_name} at price {txn.price}")

    # Apply configurable tax rate
    TAX_RATE = Decimal(0.10)  # 10% tax rate, could be configured elsewhere
    tax_amount = total_profit * TAX_RATE

    return TaxResponse(
        user_id=user_id,
        total_profit=float(total_profit),  # Convert to float for frontend compatibility
        tax_amount=float(tax_amount)      # Convert to float for frontend compatibility
    )
