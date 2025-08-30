from config import db

cart_collection = db["cart"]

def add_to_cart(user_id, product_id, quantity):
    cart_item = {"user_id": user_id, "product_id": product_id, "quantity": quantity}
    cart_collection.insert_one(cart_item)
    return cart_item

def get_cart(user_id):
    return list(cart_collection.find({"user_id": user_id}, {"_id": 0}))
