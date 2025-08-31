from config import orders_collection
from bson.objectid import ObjectId
from typing import List

def create_order(user_id: str, items: List[dict], total_price: float, payment_status: str = "pending", razorpay_order_id: str = None) -> dict:
    """
    Create a new order with optional razorpay_order_id (dummy or real)
    """
    order = {
        "user_id": user_id,
        "items": items,
        "total_price": float(total_price),
        "payment_status": payment_status,
        "razorpay_order_id": razorpay_order_id
    }
    res = orders_collection.insert_one(order)
    order["_id"] = str(res.inserted_id)
    return order
def get_orders(user_id: str) -> list:
    """
    List all orders for a given user
    """
    cursor = orders_collection.find({"user_id": user_id})
    out = []
    for o in cursor:
        o["_id"] = str(o["_id"])
        out.append(o)
    return out

def update_payment_status_by_razorpay(order_id: str, payment_status: str, payment_id: str = None):
    """
    Update the order's payment status using the dummy razorpay_order_id
    """
    orders_collection.update_one(
        {"razorpay_order_id": order_id},
        {"$set": {"payment_status": payment_status, "payment_id": payment_id}}
    )
    return orders_collection.find_one({"razorpay_order_id": order_id})