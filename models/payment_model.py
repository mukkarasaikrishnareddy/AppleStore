from config import db
from bson import ObjectId
from datetime import datetime

payments = db.payments

def create_payment(order_id, user_id, amount, status, method):
    payment = {
        "order_id": ObjectId(order_id),
        "user_id": ObjectId(user_id),
        "amount": amount,
        "status": status,
        "payment_method": method,
        "created_at": datetime.utcnow()
    }
    payments.insert_one(payment)
    return str(payment["_id"])
