from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.cart_model import add_to_cart, get_user_cart, clear_cart

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/add", methods=["POST"])
@jwt_required()
def add_item():
    data = request.json
    user_id = get_jwt_identity()
    add_to_cart(user_id, data["product_id"], data["quantity"])
    return jsonify({"message": "Item added to cart"}), 201

@cart_bp.route("/", methods=["GET"])
@jwt_required()
def view_cart():
    user_id = get_jwt_identity()
    items = get_user_cart(user_id)
    for item in items:
        item["_id"] = str(item["_id"])
    return jsonify(items), 200

@cart_bp.route("/clear", methods=["DELETE"])
@jwt_required()
def clear():
    user_id = get_jwt_identity()
    clear_cart(user_id)
    return jsonify({"message": "Cart cleared"}), 200
