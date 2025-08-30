from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user_model import create_user, find_user_by_email
import bcrypt

auth_bp = Blueprint("auth", __name__)

# Register
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing email or password"}), 400

    if find_user_by_email(data["email"]):
        return jsonify({"error": "Email already registered"}), 400

    user = create_user(data["name"], data["email"], data["password"])
    return jsonify({"message": "User registered successfully"}), 201

# Login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = find_user_by_email(data["email"])

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not bcrypt.checkpw(data["password"].encode("utf-8"), user["password"]):
        return jsonify({"error": "Invalid password"}), 401

    token = create_access_token(identity=str(user["_id"]))
    return jsonify({"token": token}), 200
