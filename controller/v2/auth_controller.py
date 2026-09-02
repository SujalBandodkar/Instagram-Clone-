from flask import request, jsonify, make_response
from functools import wraps
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, verify_jwt_in_request, get_jwt_identity, get_jwt
from controller.v2 import api
from service import register_user, login_user
from dao import get_user_by_id
import re

def get_current_user_id():
    return int(get_jwt_identity())

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request(optional=True)
            if get_jwt_identity() is None:
                return {"error": "Authentication required"}, 401
            user = get_user_by_id(int(get_jwt_identity()))
            if user is None:
                return {"error": "User not found"}, 401
            return func(*args, **kwargs)
        except Exception:
            return {"error": "Authentication required"}, 401
    return wrapper

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request(optional=True)
            if get_jwt_identity() is None:
                return {"error": "Authentication required"}, 401
            user = get_user_by_id(int(get_jwt_identity()))
            if user is None:
                return {"error": "User not found"}, 401
            claims = get_jwt()
            if claims.get("role") != "admin":
                return {"error": "Admin access required"}, 403
            return func(*args, **kwargs)
        except Exception:
            return {"error": "Authentication required"}, 401
    return wrapper

@api.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return {"error": "JSON data is required"}, 400
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")
    confirm_password = data.get("confirm_password", "")
    if not username or not email or not password or not confirm_password:
        return {"error": "All fields are required"}, 400
    if len(password) < 8:
        return {"error": "Password must be at least 8 characters long"}, 400
    if password != confirm_password:
        return {"error": "Passwords do not match"}, 400
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return {"error": "Invalid email address"}, 400
    result, status = register_user(username, email, password)
    if status != 201:
        return result, status
    return {"message": "User registered successfully"}, 201

@api.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return {"error": "JSON data is required"}, 400
    email = data.get("email", "").strip()
    password = data.get("password", "")
    if not email or not password:
        return {"error": "Email and password are mandatory"}, 400
    user = login_user(email, password)
    if not user:
        return {"error": "Invalid username or password"}, 401
    role = user.role.name if user.role else "user"
    access_token = create_access_token(identity=str(user.id), additional_claims={"username": user.username, "role": role})
    response = make_response({"message": "Login successful", "user_id": user.id, "username": user.username, "role": role}, 200)
    set_access_cookies(response, access_token)
    return response

@api.route("/logout", methods=["POST"])
@login_required
def logout():
    response = make_response({"message": "Logged out successfully"}, 200)
    unset_jwt_cookies(response)
    return response
