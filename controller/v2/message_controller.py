from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from controller.v2 import api
from controller.v2.auth_controller import login_required, get_current_user_id
from service import get_conversation_data, send_message_to_user, get_inbox_data
from dao import get_user_by_id, mark_messages_read

@api.route("/inbox", methods=["GET"])
@login_required
def inbox():
    try:
        chats = get_inbox_data(get_current_user_id())
    except Exception:
        return {"error": "Failed to load inbox"}, 500
    result = []
    for chat in chats:
        other_user = chat.get("other_user")
        last_message = chat.get("last_message")
        if other_user is None:
            continue
        result.append({
            "id": chat["conversation"].id,
            "other_user": {"id": other_user.id, "username": other_user.username},
            "last_message": {"content": last_message.content, "sent_at": last_message.sent_at} if last_message else None,
            "unread_count": getattr(chat, 'unread_count', 0)
        })
    return jsonify(result), 200

@api.route("/messages/<int:user_id>", methods=["GET"])
@login_required
def get_messages(user_id):
    if user_id == get_current_user_id():
        return {"error": "You cannot message yourself"}, 400
    other_user = get_user_by_id(user_id)
    if other_user is None:
        return {"error": "User not found"}, 404
    chat, messages = get_conversation_data(get_current_user_id(), user_id)
    return {
        "conversation_id": chat.id if chat else None,
        "messages": [{"id": m.id, "sender_id": m.sender_id, "content": m.content, "sent_at": m.sent_at, "read_at": m.read_at} for m in messages] if messages else []
    }, 200

@api.route("/messages/<int:user_id>", methods=["POST"])
@login_required
def send_message(user_id):
    if user_id == get_current_user_id():
        return {"error": "You cannot message yourself"}, 400
    other_user = get_user_by_id(user_id)
    if other_user is None:
        return {"error": "User not found"}, 404
    data = request.get_json()
    if not data:
        return {"error": "JSON data is required"}, 400
    content = data.get("content", "").strip()
    if not content:
        return {"error": "Message cannot be empty"}, 400
    send_message_to_user(get_current_user_id(), user_id, content)
    return {"message": "Message sent successfully"}, 201

@api.route("/messages/<int:user_id>/read", methods=["POST"])
@login_required
def mark_read(user_id):
    chat, _ = get_conversation_data(get_current_user_id(), user_id)
    if not chat:
        return {"error": "Conversation not found"}, 404
    mark_messages_read(chat.id, get_current_user_id())
    return {"message": "Messages marked as read"}, 200
