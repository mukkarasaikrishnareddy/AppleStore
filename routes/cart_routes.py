from flask import Blueprint, request, jsonify
from models.cart_model import add_to_cart, get_cart

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/add", methods=["POST"])
def add_cart():
    data = request.json
    if not data or not data.get("user_id") or not data.get("product_id"):
        return jsonify({"error": "Missing fields"}), 400

    cart_item = add_to_cart(data["user_id"], data["product_id"], data.get("quantity", 1))
    return jsonify({"message": "Item added to cart", "cart": cart_item}), 201

@cart_bp.route("/<user_id>", methods=["GET"])
def view_cart(user_id):
    return jsonify(get_cart(user_id)), 200
