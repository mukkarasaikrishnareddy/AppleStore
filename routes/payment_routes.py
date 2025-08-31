from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import razorpay
from config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
from models.payment_model import save_payment_record
from models.order_model import update_payment_status_by_razorpay
from utils.validators import require_fields

payment_bp = Blueprint("payment", __name__)

# initialize razorpay client
rz_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

@payment_bp.post("/create-order")
@jwt_required()
def create_order():
    data = request.get_json(force=True, silent=False)
    try:
        amount = float(data.get("amount", 0))
    except Exception:
        return jsonify({"error": "Invalid amount"}), 400

    if amount <= 0:
        return jsonify({"error": "Invalid amount"}), 400

    # Razorpay expects amount in paise
    order = rz_client.order.create({
        "amount": int(amount * 100),
        "currency": data.get("currency", "INR"),
        "payment_capture": 1
    })

    # optionally store order mapping in payments or orders (razorpay_order_id)
    user_email = get_jwt_identity()
    save_payment_record(user_email, order["id"], amount, "created")

    return jsonify({"order": order}), 201

@payment_bp.post("/verify")
@jwt_required()
def verify_payment():
    data = request.get_json(force=True, silent=False)
    try:
        require_fields(data, ["razorpay_order_id", "razorpay_payment_id", "razorpay_signature"])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    payload = {
        "razorpay_order_id": data["razorpay_order_id"],
        "razorpay_payment_id": data["razorpay_payment_id"],
        "razorpay_signature": data["razorpay_signature"]
    }

    try:
        rz_client.utility.verify_payment_signature(payload)
    except Exception:
        return jsonify({"error": "Payment signature verification failed"}), 400

    # update payment records and orders
    user_email = get_jwt_identity()
    save_payment_record(user_email, data["razorpay_order_id"], data.get("amount", 0), "paid", payment_id=data["razorpay_payment_id"])
    update_payment_status_by_razorpay(data["razorpay_order_id"], "paid", payment_id=data["razorpay_payment_id"])

    return jsonify({"message": "Payment verified successfully"}), 200
