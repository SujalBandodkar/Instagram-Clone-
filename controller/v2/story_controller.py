from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from controller.v2 import api
from controller.v2.auth_controller import login_required, get_current_user_id
from service import create_new_story, view_story_by_user
from dao import get_story_by_id, delete_story as dao_delete_story
from datetime import datetime

@api.route("/stories", methods=["POST"])
@login_required
def create_story():
    file = request.files.get("image")
    caption = request.form.get("caption", "").strip()
    if not file or not file.filename:
        return {"error": "Story image is mandatory"}, 400
    story = create_new_story(get_current_user_id(), file, caption)
    if not story:
        return {"error": "Invalid story image type"}, 400
    return {"message": "Story created successfully"}, 201

@api.route("/stories", methods=["GET"])
@login_required
def get_stories():
    from dao import get_active_stories
    try:
        stories = get_active_stories([get_current_user_id()])
    except Exception:
        return {"error": "Failed to load stories"}, 500
    return jsonify([{"id": s.id, "user_id": s.user_id, "image": s.image, "caption": s.caption, "created_at": s.created_at, "expires_at": s.expires_at} for s in stories]), 200

@api.route("/stories/<int:story_id>", methods=["GET"])
@login_required
def view_story(story_id):
    story = get_story_by_id(story_id)
    if story is None:
        return {"error": "Story not found"}, 404
    if story.expires_at <= datetime.now():
        return {"error": "Story has expired"}, 410
    view_story_by_user(story_id, get_current_user_id())
    return {
        "id": story.id,
        "user_id": story.user_id,
        "image": story.image,
        "caption": story.caption,
        "created_at": story.created_at,
        "expires_at": story.expires_at
    }, 200

@api.route("/stories/<int:story_id>", methods=["DELETE"])
@login_required
def delete_story(story_id):
    story = get_story_by_id(story_id)
    if story is None:
        return {"error": "Story not found"}, 404
    if story.user_id != get_current_user_id():
        return {"error": "You can only delete your own stories"}, 403
    dao_delete_story(story)
    return {"message": "Story deleted successfully"}, 200
