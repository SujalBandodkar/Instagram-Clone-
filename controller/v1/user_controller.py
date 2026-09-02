from flask import redirect, url_for, render_template, request, flash
from flask_jwt_extended import get_jwt_identity
from controller.v1 import controller
from controller.v1.auth_controller import login_required, get_current_user_id
from service import get_profile_data, update_profile, toggle_follow, search_content, get_followers_list, get_following_list
from dao import get_user_by_id

@controller.route("/profile/<int:user_id>", methods=["GET"])
@login_required
def profile(user_id):
    data = get_profile_data(user_id, get_current_user_id())
    if not data:
        flash("User not found", "error")
        return redirect(url_for("controller.home"))
    return render_template("profile.html", **data)

@controller.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    user = get_user_by_id(get_current_user_id())
    if user is None:
        return redirect(url_for("controller.login"))
    if request.method == "GET":
        return render_template("edit_profile.html", user=user)
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    bio = request.form.get("bio", "").strip()
    if not username:
        flash("Username is mandatory", "error")
        return redirect(url_for("controller.edit_profile"))
    if not email:
        flash("Email is mandatory", "error")
        return redirect(url_for("controller.edit_profile"))
    file = request.files.get("profile_picture")
    result, status = update_profile(user.id, username, email, bio, file)
    if status != 200:
        error_msg = result.get("error", "Profile update failed") if isinstance(result, dict) else "Profile update failed"
        flash(error_msg, "error")
        return redirect(url_for("controller.edit_profile"))
    return redirect(url_for("controller.profile", user_id=user.id))

@controller.route("/users/<int:user_id>/follow", methods=["POST"])
@login_required
def follow_user(user_id):
    if user_id == get_current_user_id():
        flash("You cannot follow yourself", "error")
        return redirect(url_for("controller.home"))
    user = get_user_by_id(user_id)
    if user is None:
        flash("User not found", "error")
        return redirect(url_for("controller.home"))
    followed = toggle_follow(get_current_user_id(), user_id)
    if not followed:
        flash("Already following this user", "error")
    return redirect(url_for("controller.profile", user_id=user_id))

@controller.route("/users/<int:user_id>/unfollow", methods=["POST"])
@login_required
def unfollow_user(user_id):
    followed = toggle_follow(get_current_user_id(), user_id)
    if followed:
        flash("You are not following this user", "error")
    return redirect(url_for("controller.profile", user_id=user_id))

@controller.route("/search", methods=["GET"])
@login_required
def search():
    query = request.args.get("q", "").strip()
    if not query:
        return render_template("search.html", users=[], posts=[], query="")
    users, posts = search_content(query)
    return render_template("search.html", users=users, posts=posts, query=query)

@controller.route("/profile/<int:user_id>/followers", methods=["GET"])
@login_required
def followers(user_id):
    data = get_followers_list(user_id)
    if not data:
        flash("User not found", "error")
        return redirect(url_for("controller.home"))
    return render_template("follow_list.html", **data)

@controller.route("/profile/<int:user_id>/following", methods=["GET"])
@login_required
def following(user_id):
    data = get_following_list(user_id)
    if not data:
        flash("User not found", "error")
        return redirect(url_for("controller.home"))
    return render_template("follow_list.html", **data)
