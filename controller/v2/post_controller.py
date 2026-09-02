from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from controller.v2 import api
from controller.v2.auth_controller import login_required, get_current_user_id
from service import get_home_feed, create_new_post, update_existing_post, add_new_comment, remove_comment
from dao import get_post_by_id, delete_post as dao_delete_post, get_like, get_all_posts, create_like, delete_like

@api.route("/feed", methods=["GET"])
@login_required
def get_feed():
    posts, stories, liked_post_ids = get_home_feed(get_current_user_id())
    return {
        "posts": [{"id": p.id, "content": p.content, "image": p.image, "user_id": p.user_id, "created_at": p.created_at} for p in posts],
        "stories": [{"id": s.id, "image": s.image, "user_id": s.user_id, "created_at": s.created_at} for s in stories],
        "liked_post_ids": liked_post_ids
    }, 200

@api.route("/posts", methods=["POST"])
@login_required
def create_post():
    content = request.form.get("content", "").strip()
    file = request.files.get("image")
    if not content and not file:
        return {"error": "Post must contain text or an image"}, 400
    post = create_new_post(get_current_user_id(), content, file)
    return {"message": "Post created successfully"}, 201

@api.route("/posts", methods=["GET"])
@login_required
def get_all_posts_route():
    posts = get_all_posts()
    result = [{"id": p.id, "user_id": p.user_id, "content": p.content, "image": p.image, "created_at": p.created_at} for p in posts]
    return jsonify(result), 200

@api.route("/posts/<int:post_id>", methods=["GET"])
@login_required
def view_post(post_id):
    post = get_post_by_id(post_id)
    if post is None:
        return {"error": "Post not found"}, 404
    is_liked = get_like(get_current_user_id(), post_id) is not None
    return {
        "id": post.id,
        "user_id": post.user_id,
        "content": post.content,
        "image": post.image,
        "created_at": post.created_at,
        "is_liked": is_liked,
        "comments": [{"id": c.id, "user_id": c.user_id, "content": c.content, "created_at": c.created_at} for c in post.comments]
    }, 200

@api.route("/posts/<int:post_id>", methods=["PUT"])
@login_required
def edit_post(post_id):
    post = get_post_by_id(post_id)
    if post is None:
        return {"error": "Post not found"}, 404
    if post.user_id != get_current_user_id():
        return {"error": "You can only edit your own posts"}, 403
    data = request.get_json()
    if not data:
        return {"error": "JSON data is required"}, 400
    content = data.get("content", "").strip()
    if not content and not post.image:
        return {"error": "Post must contain text or an image"}, 400
    update_existing_post(post, content, None)
    return {"message": "Post updated successfully"}, 200

@api.route("/posts/<int:post_id>", methods=["DELETE"])
@login_required
def delete_post(post_id):
    post = get_post_by_id(post_id)
    if post is None:
        return {"error": "Post not found"}, 404
    if post.user_id != get_current_user_id():
        return {"error": "You can only delete your own posts"}, 403
    dao_delete_post(post)
    return {"message": "Post deleted successfully"}, 200

@api.route("/posts/<int:post_id>/like", methods=["POST"])
@login_required
def like_post(post_id):
    post = get_post_by_id(post_id)
    if post is None:
        return {"error": "Post not found"}, 404
    existing = get_like(get_current_user_id(), post_id)
    if existing:
        return {"error": "Post already liked"}, 409
    create_like(get_current_user_id(), post_id)
    return {"message": "Post liked successfully"}, 201

@api.route("/posts/<int:post_id>/like", methods=["DELETE"])
@login_required
def unlike_post(post_id):
    existing = get_like(get_current_user_id(), post_id)
    if not existing:
        return {"error": "Post is not liked"}, 404
    delete_like(existing)
    return {"message": "Post unliked successfully"}, 200

@api.route("/posts/<int:post_id>/comments", methods=["POST"])
@login_required
def add_comment(post_id):
    post = get_post_by_id(post_id)
    if post is None:
        return {"error": "Post not found"}, 404
    data = request.get_json()
    if not data:
        return {"error": "JSON data is required"}, 400
    content = data.get("content", "").strip()
    if not content:
        return {"error": "Comment cannot be empty"}, 400
    add_new_comment(post_id, get_current_user_id(), content)
    return {"message": "Comment added successfully"}, 201

@api.route("/comments/<int:comment_id>", methods=["DELETE"])
@login_required
def delete_comment(comment_id):
    if not remove_comment(comment_id, get_current_user_id()):
        return {"error": "Comment not found or unauthorized"}, 403
    return {"message": "Comment deleted successfully"}, 200
