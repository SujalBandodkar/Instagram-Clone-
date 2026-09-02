from flask import redirect, url_for, render_template, request, flash
from flask_jwt_extended import get_jwt_identity
from controller.v1 import controller
from controller.v1.auth_controller import login_required, get_current_user_id
from service import create_new_story, view_story_by_user
from dao import get_story_by_id, get_active_stories_by_user, delete_story as dao_delete_story
from datetime import datetime

@controller.route("/stories/create", methods=["GET", "POST"])
@login_required
def create_story():
    if request.method == "GET":
        return render_template("story_form.html")
    file = request.files.get("image")
    caption = request.form.get("caption", "").strip()
    if not file or not file.filename:
        flash("Story image is mandatory", "error")
        return redirect(url_for("controller.create_story"))
    story = create_new_story(get_current_user_id(), file, caption)
    if not story:
        flash("Invalid story image type", "error")
        return redirect(url_for("controller.create_story"))
    return redirect(url_for("controller.home"))

@controller.route("/stories/<int:story_id>", methods=["GET"])
@login_required
def view_story(story_id):
    story = get_story_by_id(story_id)
    if story is None:
        flash("Story not found", "error")
        return redirect(url_for("controller.home"))
    if story.expires_at <= datetime.now():
        flash("Story has expired", "error")
        return redirect(url_for("controller.home"))
    view_story_by_user(story_id, get_current_user_id())
    user_stories = get_active_stories_by_user(story.user_id)
    story_index = next((i for i, s in enumerate(user_stories) if s.id == story_id), 0)
    return render_template("story.html", story=story, user_stories=user_stories, story_index=story_index)

@controller.route("/stories/<int:story_id>/delete", methods=["POST"])
@login_required
def delete_story(story_id):
    story = get_story_by_id(story_id)
    if story is None:
        flash("Story not found", "error")
        return redirect(url_for("controller.home"))
    if story.user_id != get_current_user_id():
        flash("You can only delete your own stories", "error")
        return redirect(url_for("controller.home"))
    dao_delete_story(story)
    return redirect(url_for("controller.home"))
