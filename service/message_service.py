from dao.message_dao import (
    get_conversation, create_conversation, create_message,
    get_messages, get_user_conversations
)
from dao.user_dao import get_user_by_id

def get_or_create_conversation(user1_id, user2_id):
    u1, u2 = min(user1_id, user2_id), max(user1_id, user2_id)
    chat = get_conversation(u1, u2)
    if not chat:
        chat = create_conversation(u1, u2)
    return chat

def send_message_to_user(current_user_id, other_user_id, content):
    chat = get_or_create_conversation(current_user_id, other_user_id)
    return create_message(chat.id, current_user_id, content)

def get_conversation_data(current_user_id, other_user_id):
    chat = get_or_create_conversation(current_user_id, other_user_id)
    messages = get_messages(chat.id)
    return chat, messages

def get_inbox_data(user_id):
    conversations = get_user_conversations(user_id)
    chats = []
    for conv in conversations:
        other_id = conv.user2_id if conv.user1_id == user_id else conv.user1_id
        other_user = get_user_by_id(other_id)
        if other_user is None:
            continue
        messages = get_messages(conv.id)
        last_message = messages[-1] if messages else None
        chats.append({
            "conversation": conv,
            "other_user": other_user,
            "last_message": last_message
        })
    return chats
