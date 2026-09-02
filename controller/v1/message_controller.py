from flask import redirect, url_for, render_template, request, flash
from flask_jwt_extended import get_jwt_identity
from controller.v1 import controller
from controller.v1.auth_controller import login_required, get_current_user_id
from service import get_conversation_data, send_message_to_user, get_inbox_data
from dao import get_user_by_id, mark_messages_read

@controller.route("/messages/<int:user_id>", methods=["GET", "POST"])
@login_required
def conversation(user_id):
    if user_id == get_current_user_id():
        flash("You cannot message yourself", "error")
        return redirect(url_for("controller.inbox"))
    other_user = get_user_by_id(user_id)
    if other_user is None:
        flash("User not found", "error")
        return redirect(url_for("controller.inbox"))
    if request.method == "GET":
        chat, messages = get_conversation_data(get_current_user_id(), user_id)
        return render_template("conversation.html", conversation=chat, messages=messages, other_user=other_user)
    content = request.form.get("content", "").strip()
    if not content:
        flash("Message cannot be empty", "error")
        return redirect(url_for("controller.conversation", user_id=user_id))
    send_message_to_user(get_current_user_id(), user_id, content)
    return redirect(url_for("controller.conversation", user_id=user_id))

@controller.route("/messages/<int:user_id>/read", methods=["POST"])
@login_required
def mark_messages_read_route(user_id):
    chat, _ = get_conversation_data(get_current_user_id(), user_id)
    if not chat:
        flash("Conversation not found", "error")
        return redirect(url_for("controller.inbox"))
    mark_messages_read(chat.id, get_current_user_id())
    return redirect(url_for("controller.conversation", user_id=user_id))

@controller.route("/inbox", methods=["GET"])
@login_required
def inbox():
    chats = get_inbox_data(get_current_user_id())
    return render_template("inbox.html", chats=chats)
