from flask import Blueprint, request, jsonify
from models.product_model import add_product, get_all_products

product_bp = Blueprint("products", __name__)

@product_bp.route("/", methods=["GET"])
def get_products():
    return jsonify(get_all_products()), 200

@product_bp.route("/add", methods=["POST"])
def create_product():
    data = request.json
    if not data or not data.get("name") or not data.get("price"):
        return jsonify({"error": "Missing fields"}), 400

    product = add_product(data["name"], data["price"], data.get("stock", 0))
    return jsonify({"message": "Product added successfully", "product": product}), 201
