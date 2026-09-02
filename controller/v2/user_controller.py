from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from controller.v2 import api
from controller.v2.auth_controller import login_required, get_current_user_id
from dao import get_all_users, get_user_by_id
from service import get_profile_data, update_profile, toggle_follow, search_content, get_followers_list, get_following_list

@api.route("/users", methods=["GET"])
@login_required
def get_users():
    users = get_all_users()
    result = [{"id": u.id, "username": u.username, "email": u.email, "bio": u.bio, "profile_picture": u.profile_picture} for u in users]
    return jsonify(result), 200

@api.route("/users/<int:user_id>", methods=["GET"])
@login_required
def get_user_profile(user_id):
    data = get_profile_data(user_id, get_current_user_id())
    if not data:
        return {"error": "User not found"}, 404
    user = data.get("user")
    if not user:
        return {"error": "User not found"}, 404
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "bio": user.bio,
        "profile_picture": user.profile_picture,
        "posts_count": len(data.get("posts", [])),
        "followers_count": data.get("followers_count", 0),
        "following_count": data.get("following_count", 0)
    }, 200

@api.route("/users/profile", methods=["PUT"])
@login_required
def edit_profile():
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    bio = request.form.get("bio", "").strip()
    if not username:
        return {"error": "Username is mandatory"}, 400
    if not email:
        return {"error": "Email is mandatory"}, 400
    file = request.files.get("profile_picture")
    result, status = update_profile(get_current_user_id(), username, email, bio, file)
    if status != 200:
        return result, status
    return {"message": "Profile updated successfully"}, 200

@api.route("/users/<int:user_id>/follow", methods=["POST"])
@login_required
def follow_user(user_id):
    if user_id == get_current_user_id():
        return {"error": "You cannot follow yourself"}, 400
    user = get_user_by_id(user_id)
    if user is None:
        return {"error": "User not found"}, 404
    followed = toggle_follow(get_current_user_id(), user_id)
    if not followed:
        return {"error": "Already following this user"}, 409
    return {"message": "User followed successfully"}, 201

@api.route("/users/<int:user_id>/follow", methods=["DELETE"])
@login_required
def unfollow_user(user_id):
    followed = toggle_follow(get_current_user_id(), user_id)
    if followed:
        return {"error": "You are not following this user"}, 404
    return {"message": "User unfollowed successfully"}, 200

@api.route("/search", methods=["GET"])
@login_required
def search():
    query = request.args.get("q", "").strip()
    if not query:
        return {"error": "Search query is mandatory"}, 400
    users, posts = search_content(query)
    return {
        "users": [{"id": u.id, "username": u.username, "profile_picture": u.profile_picture} for u in users],
        "posts": [{"id": p.id, "content": p.content, "image": p.image} for p in posts]
    }, 200

@api.route("/users/<int:user_id>/followers", methods=["GET"])
@login_required
def get_followers(user_id):
    data = get_followers_list(user_id)
    if not data:
        return {"error": "User not found"}, 404
    return {
        "user": {"id": data["user"].id, "username": data["user"].username},
        "followers": [{"id": u.id, "username": u.username, "bio": u.bio, "profile_picture": u.profile_picture} for u in data["users"]]
    }, 200

@api.route("/users/<int:user_id>/following", methods=["GET"])
@login_required
def get_following(user_id):
    data = get_following_list(user_id)
    if not data:
        return {"error": "User not found"}, 404
    return {
        "user": {"id": data["user"].id, "username": data["user"].username},
        "following": [{"id": u.id, "username": u.username, "bio": u.bio, "profile_picture": u.profile_picture} for u in data["users"]]
    }, 200
