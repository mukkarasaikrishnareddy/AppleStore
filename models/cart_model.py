from typing import List
from bson.objectid import ObjectId
from config import carts_collection, products_collection

def _ensure_cart(user_id: str) -> dict:
    cart = carts_collection.find_one({"user_id": user_id})
    if not cart:
        cart = {"user_id": user_id, "items": []}
        carts_collection.insert_one(cart)
    return cart

def get_cart(user_id: str) -> dict:
    cart = _ensure_cart(user_id)
    detailed = []
    for it in cart.get("items", []):
        try:
            prod = products_collection.find_one({"_id": ObjectId(it["product_id"])})
        except Exception:
            prod = None
        if prod:
            price = float(prod.get("price", 0.0))
            qty = int(it.get("quantity", 0))
            detailed.append({
                "product_id": it["product_id"],
                "name": prod.get("name"),
                "price": price,
                "quantity": qty,
                "subtotal": price * qty
            })
    total = sum(i["subtotal"] for i in detailed)
    return {"user_id": user_id, "items": detailed, "total": total}

def add_item(user_id: str, product_id: str, qty: int) -> dict:
    # push if not present, else increment
    carts_collection.update_one(
        {"user_id": user_id, "items.product_id": {"$ne": product_id}},
        {"$push": {"items": {"product_id": product_id, "quantity": qty}}},
        upsert=True
    )
    carts_collection.update_one(
        {"user_id": user_id, "items.product_id": product_id},
        {"$inc": {"items.$.quantity": qty}}
    )
    return get_cart(user_id)

def update_item(user_id: str, product_id: str, qty: int) -> dict:
    if qty <= 0:
        remove_item(user_id, product_id)
        return get_cart(user_id)
    carts_collection.update_one(
        {"user_id": user_id, "items.product_id": product_id},
        {"$set": {"items.$.quantity": qty}}
    )
    return get_cart(user_id)

def remove_item(user_id: str, product_id: str) -> dict:
    carts_collection.update_one({"user_id": user_id}, {"$pull": {"items": {"product_id": product_id}}})
    return get_cart(user_id)

def clear_cart(user_id: str) -> dict:
    carts_collection.update_one({"user_id": user_id}, {"$set": {"items": []}}, upsert=True)
    return get_cart(user_id)
