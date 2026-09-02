from config.database import db
from models import Conversations, Messages

def get_conversation(user1_id, user2_id):
    return Conversations.query.filter_by(user1_id=user1_id, user2_id=user2_id).first()

def create_conversation(user1_id, user2_id):
    chat = Conversations(user1_id, user2_id)
    db.session.add(chat)
    db.session.commit()
    return chat

def get_messages(conversation_id):
    return Messages.query.filter_by(conversation_id=conversation_id).order_by(Messages.sent_at.asc()).all()

def create_message(conversation_id, sender_id, content):
    message = Messages(conversation_id, sender_id, content)
    db.session.add(message)
    db.session.commit()
    return message

def get_user_conversations(user_id):
    return Conversations.query.filter(
        (Conversations.user1_id == user_id) | (Conversations.user2_id == user_id)
    ).order_by(Conversations.updated_at.desc()).all()

def mark_messages_read(conversation_id, current_user_id):
    from datetime import datetime
    messages = Messages.query.filter(
        Messages.conversation_id == conversation_id,
        Messages.sender_id != current_user_id,
        Messages.read_at.is_(None)
    ).all()
    for message in messages:
        message.read_at = datetime.now()
    db.session.commit()
