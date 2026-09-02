from flask import redirect, url_for, render_template, request, make_response, flash
from functools import wraps
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, verify_jwt_in_request, get_jwt_identity, get_jwt
from models import RegisterForm
from service import register_user, login_user
from dao import get_user_by_id
from controller.v1 import controller

def get_current_user_id():
    return int(get_jwt_identity())

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request(optional=True)
            if get_jwt_identity() is None:
                return redirect(url_for("controller.login"))
            user = get_user_by_id(int(get_jwt_identity()))
            if user is None:
                response = make_response(redirect(url_for("controller.login")))
                unset_jwt_cookies(response)
                return response
            return func(*args, **kwargs)
        except Exception:
            return redirect(url_for("controller.login"))
    return wrapper

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request(optional=True)
            if get_jwt_identity() is None:
                return redirect(url_for("controller.login"))
            user = get_user_by_id(int(get_jwt_identity()))
            if user is None:
                response = make_response(redirect(url_for("controller.login")))
                unset_jwt_cookies(response)
                return response
            claims = get_jwt()
            if claims.get("role") != "admin":
                flash("Admin access required", "error")
                return redirect(url_for("controller.home"))
            return func(*args, **kwargs)
        except Exception:
            return redirect(url_for("controller.login"))
    return wrapper

@controller.context_processor
def inject_current_user():
    try:
        verify_jwt_in_request()
        user_id = int(get_jwt_identity())
        user = get_user_by_id(user_id)
        claims = get_jwt()
        return {"current_user": user, "current_user_id": user_id, "current_role": claims.get("role")}
    except Exception:
        return {"current_user": None, "current_user_id": None, "current_role": None}

@controller.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip()
        password = form.password.data
        result, status = register_user(username, email, password)
        if status != 201:
            error_msg = result.get("error", "Registration failed") if isinstance(result, dict) else "Registration failed"
            flash(error_msg, "error")
            return redirect(url_for("controller.register"))
        return redirect(url_for("controller.login"))
    return render_template("register.html", form=form)

@controller.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    if not email or not password:
        flash("Email and password are mandatory", "error")
        return redirect(url_for("controller.login"))
    user = login_user(email, password)
    if not user:
        flash("Invalid email or password", "error")
        return redirect(url_for("controller.login"))
    role = user.role.name if user.role else "user"
    access_token = create_access_token(identity=str(user.id), additional_claims={"username": user.username, "role": role})
    response = make_response(redirect(url_for("controller.home")))
    set_access_cookies(response, access_token)
    return response

@controller.route("/logout", methods=["GET"])
@login_required
def logout():
    response = make_response(redirect(url_for("controller.login")))
    unset_jwt_cookies(response)
    return response
