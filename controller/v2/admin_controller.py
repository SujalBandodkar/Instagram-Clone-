from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from controller.v2 import api
from controller.v2.auth_controller import admin_required, get_current_user_id
from dao import get_all_users, get_all_posts, get_user_by_id, get_post_by_id, delete_post as dao_delete_post
from config.database import db

@api.route("/admin/dashboard", methods=["GET"])
@admin_required
def admin_dashboard():
    users = get_all_users()
    posts = get_all_posts()
    return {
        "user_count": len(users),
        "post_count": len(posts),
        "users": [{"id": u.id, "username": u.username, "email": u.email} for u in users],
        "posts": [{"id": p.id, "user_id": p.user_id, "content": p.content} for p in posts]
    }, 200

@api.route("/admin/users/<int:user_id>", methods=["DELETE"])
@admin_required
def admin_delete_user(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        return {"error": "User not found"}, 404
    if user.id == get_current_user_id():
        return {"error": "Admin cannot delete their own account"}, 400
    try:
        db.session.delete(user)
        db.session.commit()
    except Exception:
        return {"error": "Cannot delete user. User may have existing posts or messages."}, 400
    return {"message": "User deleted successfully"}, 200

@api.route("/admin/posts/<int:post_id>", methods=["DELETE"])
@admin_required
def admin_delete_post(post_id):
    post = get_post_by_id(post_id)
    if post is None:
        return {"error": "Post not found"}, 404
    dao_delete_post(post)
    return {"message": "Post deleted successfully"}, 200
