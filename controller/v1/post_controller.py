from flask import redirect, url_for, render_template, request, flash, jsonify
from flask_jwt_extended import get_jwt_identity
import random
from controller.v1 import controller
from controller.v1.auth_controller import login_required, get_current_user_id
from service import get_home_feed, get_home_feed_page, create_new_post, update_existing_post, add_new_comment, remove_comment
from dao import get_post_by_id, delete_post as dao_delete_post, get_like, get_active_stories
from dao.user_dao import get_following_ids

PER_PAGE = 10

@controller.route("/", methods=["GET"])
@controller.route("/home", methods=["GET"])
@login_required
def home():
    seed = random.randint(1, 999999)
    posts, liked_post_ids = get_home_feed_page(get_current_user_id(), 1, PER_PAGE, seed)
    following_ids = get_following_ids(get_current_user_id())
    following_ids.append(get_current_user_id())
    stories = get_active_stories(following_ids)
    return render_template("home.html", posts=posts, stories=stories, liked_post_ids=liked_post_ids, seed=seed, page=1)

@controller.route("/api/posts/page", methods=["GET"])
@login_required
def load_posts():
    page = request.args.get("page", 1, type=int)
    seed = request.args.get("seed", 0, type=int)
    posts, liked_post_ids = get_home_feed_page(get_current_user_id(), page, PER_PAGE, seed)
    return jsonify([{
        "id": p.id,
        "content": p.content,
        "image": url_for('static', filename='uploads/' + p.image) if p.image else None,
        "created_at": p.created_at.strftime('%b %d'),
        "author": {
            "id": p.post_author.id,
            "username": p.post_author.username,
            "profile_picture": url_for('static', filename='uploads/' + p.post_author.profile_picture) if p.post_author.profile_picture else None
        },
        "likes_count": len(p.likes),
        "comments_count": len(p.comments),
        "is_liked": p.id in liked_post_ids
    } for p in posts])

@controller.route("/posts/create", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "GET":
        return render_template("post_form.html")
    content = request.form.get("content", "").strip()
    file = request.files.get("image")
    if not content and not file:
        flash("Post must contain text or an image", "error")
        return redirect(url_for("controller.create_post"))
    create_new_post(get_current_user_id(), content, file)
    return redirect(url_for("controller.home"))

@controller.route("/posts/<int:post_id>", methods=["GET"])
@login_required
def view_post(post_id):
    post = get_post_by_id(post_id)
    if post is None:
        flash("Post not found", "error")
        return redirect(url_for("controller.home"))
    is_liked = get_like(get_current_user_id(), post_id) is not None
    return render_template("post.html", post=post, is_liked=is_liked)

@controller.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = get_post_by_id(post_id)
    if post is None:
        flash("Post not found", "error")
        return redirect(url_for("controller.home"))
    if post.user_id != get_current_user_id():
        flash("You can only edit your own posts", "error")
        return redirect(url_for("controller.view_post", post_id=post_id))
    if request.method == "GET":
        return render_template("edit_post.html", post=post)
    content = request.form.get("content", "").strip()
    file = request.files.get("image")
    if not content and not file and not post.image:
        flash("Post must contain text or an image", "error")
        return redirect(url_for("controller.edit_post", post_id=post_id))
    update_existing_post(post, content, file)
    return redirect(url_for("controller.view_post", post_id=post.id))

@controller.route("/posts/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = get_post_by_id(post_id)
    if post is None:
        flash("Post not found", "error")
        return redirect(url_for("controller.home"))
    if post.user_id != get_current_user_id():
        flash("You can only delete your own posts", "error")
        return redirect(url_for("controller.home"))
    dao_delete_post(post)
    return redirect(url_for("controller.home"))

@controller.route("/posts/<int:post_id>/like", methods=["POST"])
@login_required
def like_post(post_id):
    post = get_post_by_id(post_id)
    if post is None:
        flash("Post not found", "error")
        return redirect(url_for("controller.home"))
    existing = get_like(get_current_user_id(), post_id)
    if existing:
        return redirect(request.referrer or url_for("controller.home"))
    from dao import create_like
    create_like(get_current_user_id(), post_id)
    return redirect(request.referrer or url_for("controller.home"))

@controller.route("/posts/<int:post_id>/unlike", methods=["POST"])
@login_required
def unlike_post(post_id):
    existing = get_like(get_current_user_id(), post_id)
    if not existing:
        return redirect(request.referrer or url_for("controller.home"))
    from dao import delete_like
    delete_like(existing)
    return redirect(request.referrer or url_for("controller.home"))

@controller.route("/posts/<int:post_id>/comments", methods=["POST"])
@login_required
def add_comment(post_id):
    post = get_post_by_id(post_id)
    if post is None:
        flash("Post not found", "error")
        return redirect(url_for("controller.home"))
    content = request.form.get("content", "").strip()
    if not content:
        flash("Comment cannot be empty", "error")
        return redirect(url_for("controller.view_post", post_id=post_id))
    add_new_comment(post_id, get_current_user_id(), content)
    return redirect(url_for("controller.view_post", post_id=post_id))

@controller.route("/comments/<int:comment_id>/delete", methods=["POST"])
@login_required
def delete_comment(comment_id):
    from dao import get_comment_by_id
    comment = get_comment_by_id(comment_id)
    if not comment:
        flash("Comment not found", "error")
        return redirect(url_for("controller.home"))
    post_id = comment.post_id
    if not remove_comment(comment_id, get_current_user_id()):
        flash("You cannot delete this comment", "error")
        return redirect(url_for("controller.view_post", post_id=post_id))
    return redirect(url_for("controller.view_post", post_id=post_id))
