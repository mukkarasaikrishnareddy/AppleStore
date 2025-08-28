from flask import Blueprint, request, jsonify
from models.product_model import add_product, get_all_products

product_bp = Blueprint("products", __name__)

@product_bp.route("/", methods=["POST"])
def create_product():
    data = request.json
    product_id = add_product(data["name"], data["description"], data["price"], data["stock"])
    return jsonify({"message": "Product added", "product_id": product_id}), 201

@product_bp.route("/", methods=["GET"])
def list_products():
    products = get_all_products()
    for product in products:
        product["_id"] = str(product["_id"])
    return jsonify(products), 200
