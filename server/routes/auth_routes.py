import re
from datetime import datetime, timezone

from flask import Blueprint, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from config import db

auth_bp = Blueprint("auth_bp", __name__)


def valid_email(email):
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email) is not None


@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    if len(name) < 2:
        return jsonify({
            "success": False,
            "message": "Please enter your name"
        }), 400

    if not valid_email(email):
        return jsonify({
            "success": False,
            "message": "Please enter a valid email address"
        }), 400

    if len(password) < 6:
        return jsonify({
            "success": False,
            "message": "Password must contain at least 6 characters"
        }), 400

    if db.users.find_one({"email": email}):
        return jsonify({
            "success": False,
            "message": "An account with this email already exists"
        }), 409

    user_data = {
        "name": name,
        "email": email,
        "password": generate_password_hash(password),
        "createdAt": datetime.now(timezone.utc).isoformat()
    }

    result = db.users.insert_one(user_data)

    session.clear()
    session.permanent = True
    session["user_id"] = str(result.inserted_id)
    session["user_name"] = name
    session["user_email"] = email

    return jsonify({
        "success": True,
        "message": "Account created successfully",
        "user": {
            "name": name,
            "email": email
        }
    }), 201


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    user = db.users.find_one({"email": email})

    if not user or not check_password_hash(user["password"], password):
        return jsonify({
            "success": False,
            "message": "Incorrect email or password"
        }), 401

    session.clear()
    session.permanent = True
    session["user_id"] = str(user["_id"])
    session["user_name"] = user["name"]
    session["user_email"] = user["email"]

    return jsonify({
        "success": True,
        "message": "Login successful",
        "user": {
            "name": user["name"],
            "email": user["email"]
        }
    })


@auth_bp.route("/api/auth/me", methods=["GET"])
def current_user():
    if not session.get("user_id"):
        return jsonify({
            "success": False,
            "message": "Not logged in"
        }), 401

    return jsonify({
        "success": True,
        "user": {
            "name": session.get("user_name"),
            "email": session.get("user_email")
        }
    })


@auth_bp.route("/api/auth/logout", methods=["POST"])
def logout():
    session.clear()

    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    })