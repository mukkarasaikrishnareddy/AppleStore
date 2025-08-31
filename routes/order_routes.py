from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.order_model import create_order, get_orders

order_bp = Blueprint("orders", __name__)

@order_bp.post("/create")
@jwt_required()
def create():
    """
    Create an order from the user's cart
    """
    user_email = get_jwt_identity()
    data = request.get_json(force=True, silent=False)

    items = data.get("items", [])
    total_price = data.get("total_price", 0)

    if not items or total_price <= 0:
        return jsonify({"error": "No items or invalid total_price"}), 400

    # Create order with pending payment
    order = create_order(user_email, items, total_price, payment_status="pending")

    return jsonify(order), 201


@order_bp.get("/")
@jwt_required()
def list_orders():
    """
    List all orders for the logged-in user
    """
    user_email = get_jwt_identity()
    return jsonify(get_orders(user_email)), 200