from config import db
from bson import ObjectId

cart = db.cart

def add_to_cart(user_id, product_id, quantity):
    cart_item = cart.find_one({"user_id": ObjectId(user_id), "product_id": ObjectId(product_id)})
    if cart_item:
        cart.update_one({"_id": cart_item["_id"]}, {"$inc": {"quantity": quantity}})
    else:
        cart.insert_one({
            "user_id": ObjectId(user_id),
            "product_id": ObjectId(product_id),
            "quantity": quantity
        })

def get_user_cart(user_id):
    return list(cart.find({"user_id": ObjectId(user_id)}))

def clear_cart(user_id):
    cart.delete_many({"user_id": ObjectId(user_id)})
