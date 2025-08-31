from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user_model import create_user, find_user_by_email, check_password
from utils.validators import require_fields
from datetime import timedelta

auth_bp = Blueprint("auth", __name__)

# ---------------- REGISTER ----------------
@auth_bp.post("/register")
def register():
    data = request.get_json(force=True, silent=False)
    try:
        require_fields(data, ["name", "email", "password"])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if find_user_by_email(data["email"]):
        return jsonify({"error": "Email already registered"}), 409

    user = create_user(data["name"], data["email"], data["password"])
    access = create_access_token(identity=user["email"], expires_delta=timedelta(hours=12))

    return jsonify({"user": user, "access_token": access}), 201
# ---------------- LOGIN ----------------
@auth_bp.post("/login")
def login():
    data = request.get_json(force=True, silent=False)
    try:
        require_fields(data, ["email", "password"])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    user_doc = find_user_by_email(data["email"])
    if not user_doc:
        return jsonify({"error": "Invalid email or password"}), 401

    if not check_password(data["password"], user_doc["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    # Build a clean user dict to return
    user_safe = {
        "id": str(user_doc["_id"]),
        "name": user_doc["name"],
        "email": user_doc["email"],
        "role": user_doc.get("role", "customer")
    }

    access = create_access_token(identity=user_safe["email"], expires_delta=timedelta(hours=12))

    return jsonify({"message": "Login successful", "user": user_safe, "access_token": access}), 200