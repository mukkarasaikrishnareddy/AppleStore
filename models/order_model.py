from config import db
from bson import ObjectId
from datetime import datetime

orders = db.orders

def create_order(user_id, items, total_price):
    order = {
        "user_id": ObjectId(user_id),
        "items": items,
        "total_price": total_price,
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    orders.insert_one(order)
    return str(order["_id"])

def update_order_status(order_id, status):
    orders.update_one({"_id": ObjectId(order_id)}, {"$set": {"status": status}})
