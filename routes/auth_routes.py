from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user_model import create_user, find_user_by_email
import bcrypt

auth_bp = Blueprint("auth", __name__)

# Register
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    if find_user_by_email(data["email"]):
        return jsonify({"error": "Email already registered"}), 400

    create_user(data["full_name"], data["email"], data["password"])
    return jsonify({"message": "Registration successful"}), 201

# Login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = find_user_by_email(data["email"])

    if not user or not bcrypt.checkpw(data["password"].encode("utf-8"), user["password"].encode("utf-8")):
        return jsonify({"error": "Invalid email or password"}), 401

    # Create JWT token
    access_token = create_access_token(identity={"id": user["id"], "email": user["email"]})
    return jsonify({"access_token": access_token}), 200