from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.cart_model import get_user_cart, clear_cart
from models.order_model import create_order

order_bp = Blueprint("orders", __name__)

@order_bp.route("/checkout", methods=["POST"])
@jwt_required()
def checkout():
    user_id = get_jwt_identity()
    cart_items = get_user_cart(user_id)
    if not cart_items:
        return jsonify({"error": "Cart is empty"}), 400
    total_price = sum(item["quantity"] * 1000 for item in cart_items)  # Simulated pricing
    order_id = create_order(user_id, cart_items, total_price)
    clear_cart(user_id)
    return jsonify({"message": "Order created", "order_id": order_id}), 201
