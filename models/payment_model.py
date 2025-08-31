from config import payments_collection

def save_payment_record(user_id: str, razorpay_order_id: str, amount: float, status: str, payment_id: str = None):
    rec = {
        "user_id": user_id,
        "razorpay_order_id": razorpay_order_id,
        "payment_id": payment_id,
        "amount": float(amount),
        "status": status
    }
    payments_collection.insert_one(rec)
    return rec
