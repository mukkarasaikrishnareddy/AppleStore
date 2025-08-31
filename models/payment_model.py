from config import payments_collection

def save_payment_record(user_id: str, razorpay_order_id: str, amount: float, status: str, internal_order_id: str = None, payment_id: str = None):
    """
    Save a payment record and optionally link it to an internal order.
    """
    rec = {
        "user_id": user_id,
        "razorpay_order_id": razorpay_order_id,
        "payment_id": payment_id,
        "internal_order_id": internal_order_id,
        "amount": float(amount),
        "status": status
    }
    payments_collection.insert_one(rec)
    return rec