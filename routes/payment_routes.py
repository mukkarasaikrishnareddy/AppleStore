import random
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.payment_model import create_payment
from models.order_model import update_order_status
from config import db
from bson import ObjectId
from datetime import datetime

payment_bp = Blueprint("payment", __name__)

@payment_bp.route("/pay", methods=["POST"])
@jwt_required()
def make_payment():
    user_id = get_jwt_identity()
    data = request.json
    order_id = data.get("order_id")
    payment_method = data.get("payment_method", "card")

    order = db.orders.find_one({"_id": ObjectId(order_id), "user_id": ObjectId(user_id)})
    if not order:
        return jsonify({"error": "Order not found"}), 404

    if order.get("status") == "paid":
        return jsonify({"error": "Order already paid"}), 400

    payment_success = random.choice([True, False])
    payment_status = "success" if payment_success else "failed"

    create_payment(order_id, user_id, order["total_price"], payment_status, payment_method)

    if payment_success:
        update_order_status(order_id, "paid")
        return jsonify({"message": "Payment successful", "order_status": "paid"}), 200
    else:
        update_order_status(order_id, "payment_failed")
        return jsonify({"message": "Payment failed", "order_status": "payment_failed"}), 400
