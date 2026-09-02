from flask import redirect, url_for, render_template, request, flash
from flask_jwt_extended import get_jwt_identity
from controller.v1 import controller
from controller.v1.auth_controller import admin_required, get_current_user_id
from dao import get_all_users, get_all_posts, get_user_by_id, get_post_by_id, delete_post as dao_delete_post
from config.database import db

@controller.route("/admin", methods=["GET"])
@admin_required
def admin_dashboard():
    users = get_all_users()
    posts = get_all_posts()
    return render_template("admin_dashboard.html", users=users, posts=posts)

@controller.route("/admin/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def admin_delete_user(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        flash("User not found", "error")
        return redirect(url_for("controller.admin_dashboard"))
    if user.id == get_current_user_id():
        flash("Admin cannot delete their own account", "error")
        return redirect(url_for("controller.admin_dashboard"))
    try:
        db.session.delete(user)
        db.session.commit()
    except Exception:
        flash("Cannot delete user. User may have existing posts or messages.", "error")
    return redirect(url_for("controller.admin_dashboard"))

@controller.route("/admin/posts/<int:post_id>/delete", methods=["POST"])
@admin_required
def admin_delete_post(post_id):
    post = get_post_by_id(post_id)
    if post is None:
        flash("Post not found", "error")
        return redirect(url_for("controller.admin_dashboard"))
    dao_delete_post(post)
    return redirect(url_for("controller.admin_dashboard"))
