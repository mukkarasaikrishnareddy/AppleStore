from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.cart_model import get_cart, add_item, update_item, remove_item, clear_cart
from utils.validators import require_fields

cart_bp = Blueprint("cart", __name__)

@cart_bp.get("/")
@jwt_required()
def get_my_cart():
    user_email = get_jwt_identity()
    return jsonify(get_cart(user_email)), 200

@cart_bp.post("/items")
@jwt_required()
def add_to_cart():
    user_email = get_jwt_identity()
    data = request.get_json(force=True, silent=False)
    try:
        require_fields(data, ["product_id", "quantity"])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    cart = add_item(user_email, data["product_id"], int(data["quantity"]))
    return jsonify(cart), 200

@cart_bp.put("/items/<product_id>")
@jwt_required()
def update_cart_item(product_id):
    user_email = get_jwt_identity()
    data = request.get_json(force=True, silent=False)
    try:
        require_fields(data, ["quantity"])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    cart = update_item(user_email, product_id, int(data["quantity"]))
    return jsonify(cart), 200

@cart_bp.delete("/items/<product_id>")
@jwt_required()
def delete_cart_item(product_id):
    user_email = get_jwt_identity()
    cart = remove_item(user_email, product_id)
    return jsonify(cart), 200

@cart_bp.delete("/clear")
@jwt_required()
def clear_my_cart():
    user_email = get_jwt_identity()
    cart = clear_cart(user_email)
    return jsonify(cart), 200
