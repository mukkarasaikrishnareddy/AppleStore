from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.payment_model import save_payment_record
from models.order_model import update_payment_status_by_razorpay
from utils.validators import require_fields
import uuid

payment_bp = Blueprint("payment", __name__)
# ---------------- CREATE DUMMY PAYMENT ORDER ----------------
@payment_bp.post("/initate")
@jwt_required()
def create_order():
    data = request.get_json(force=True, silent=False)
    try:
        require_fields(data, ["amount", "order_id"])
        amount = float(data["amount"])
    except (ValueError, KeyError):
        return jsonify({"error": "Invalid data"}), 400

    if amount <= 0:
        return jsonify({"error": "Amount must be greater than 0"}), 400

    # Generate a dummy "Razorpay" order ID
    dummy_order_id = "payment_" + str(uuid.uuid4())

    user_email = get_jwt_identity()

    # Save dummy payment record
    save_payment_record(
        user_email,
        dummy_order_id,
        amount,
        "created",
        internal_order_id=data["order_id"]
    )
    # Update internal order payment status to "pending"
    # NOTE: Pass the dummy_order_id as first positional argument
    update_payment_status_by_razorpay(dummy_order_id, "pending")

    return jsonify({
        "razorpay_order": {
            "id": dummy_order_id,
            "amount": int(amount * 100),  # in paise
            "currency": data.get("currency", "INR"),
            "status": "created"
        }
    }), 201
# ---------------- VERIFY DUMMY PAYMENT ----------------
@payment_bp.post("/verify")
@jwt_required()
def verify_payment():
    data = request.get_json(force=True, silent=False)
    try:
        require_fields(data, ["razorpay_order_id", "razorpay_payment_id", "amount"])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    user_email = get_jwt_identity()

    # Mark payment as "paid" in your dummy DB
    save_payment_record(
        user_email,
        data["razorpay_order_id"],
        data.get("amount", 0),
        "paid",
        payment_id=data["razorpay_payment_id"]
    )

    # Update internal order payment status to "paid"
    update_payment_status_by_razorpay(
        data["razorpay_order_id"],  # first positional argument
        "paid",
        payment_id=data["razorpay_payment_id"]
    )

    return jsonify({"message": "Payment verified successfully"}), 200