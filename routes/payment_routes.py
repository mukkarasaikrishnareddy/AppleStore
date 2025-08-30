import razorpay
from flask import Blueprint, request, jsonify
from config import db, RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId

payment_bp = Blueprint("payment", __name__)

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# ===============================
# 1. CREATE PAYMENT ORDER
# ===============================
@payment_bp.route("/create-order", methods=["POST"])
@jwt_required()
def create_order():
    try:
        data = request.json
        amount = data.get("amount")

        if not amount or amount <= 0:
            return jsonify({"error": "Invalid amount"}), 400

        # Create Razorpay order
        order = razorpay_client.order.create({
            "amount": amount * 100,  # Convert to paise
            "currency": "INR",
            "payment_capture": "1"
        })

        # Save order in DB
        payment_data = {
            "user_id": get_jwt_identity(),
            "order_id": order["id"],
            "amount": amount,
            "status": "created"
        }
        db.payments.insert_one(payment_data)

        return jsonify({
            "message": "Order created successfully",
            "order": order
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ===============================
# 2. VERIFY PAYMENT
# ===============================
@payment_bp.route("/verify", methods=["POST"])
@jwt_required()
def verify_payment():
    try:
        data = request.json
        order_id = data.get("order_id")
        payment_id = data.get("payment_id")
        signature = data.get("signature")

        if not order_id or not payment_id or not signature:
            return jsonify({"error": "Missing payment details"}), 400

        # Verify payment signature
        try:
            razorpay_client.utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature
            })
        except:
            return jsonify({"error": "Payment verification failed"}), 400

        # Update payment status in DB
        db.payments.update_one(
            {"order_id": order_id},
            {"$set": {"status": "paid", "payment_id": payment_id}}
        )

        return jsonify({"message": "Payment verified successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ===============================
# 3. GET PAYMENT HISTORY
# ===============================
@payment_bp.route("/history", methods=["GET"])
@jwt_required()
def payment_history():
    try:
        user_id = get_jwt_identity()
        payments = list(db.payments.find({"user_id": user_id}, {"_id": 0}))
        return jsonify(payments), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
