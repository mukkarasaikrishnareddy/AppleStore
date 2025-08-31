from flask import Blueprint, request, jsonify
from models.product_model import list_products, get_product, create_product, update_product, delete_product
from utils.validators import require_fields

product_bp = Blueprint("products", __name__)

@product_bp.get("/")
def list_all():
    q = request.args.get("q")
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", 20))
    except ValueError:
        return jsonify({"error": "Invalid pagination"}), 400

    skip = (page - 1) * size
    items = list_products(skip=skip, limit=size, q=q)
    return jsonify({"items": items, "page": page, "size": size}), 200

@product_bp.get("/<product_id>")
def get_one(product_id):
    prod = get_product(product_id)
    if not prod:
        return jsonify({"error": "Not found"}), 404
    return jsonify(prod), 200

@product_bp.post("/")
def create_one():
    data = request.get_json(force=True, silent=False)
    try:
        require_fields(data, ["name", "price"])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    prod = create_product(data)
    return jsonify(prod), 201

@product_bp.put("/<product_id>")
def update_one(product_id):
    data = request.get_json(force=True, silent=False)
    prod = update_product(product_id, data)
    if not prod:
        return jsonify({"error": "Not found"}), 404
    return jsonify(prod), 200

@product_bp.delete("/<product_id>")
def delete_one(product_id):
    ok = delete_product(product_id)
    if not ok:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"deleted": True}), 200
