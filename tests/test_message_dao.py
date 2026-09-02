from dao.message_dao import (
    get_conversation, create_conversation, get_messages, create_message,
    get_user_conversations, mark_messages_read
)
from models import Conversations, Messages, Users, Roles

def _create_users(db):
    role = Roles(name="user")
    db.session.add(role)
    db.session.commit()
    user1 = Users(role_id=role.id, username="u1", email="u1@test.com", password_hash="h1")
    user2 = Users(role_id=role.id, username="u2", email="u2@test.com", password_hash="h2")
    db.session.add_all([user1, user2])
    db.session.commit()
    return user1, user2

def test_get_conversation(app, db):
    with app.app_context():
        user1, user2 = _create_users(db)
        conv = Conversations(user1_id=user1.id, user2_id=user2.id)
        db.session.add(conv)
        db.session.commit()
        result = get_conversation(user1.id, user2.id)
        assert result is not None
        assert result.user1_id == user1.id

def test_get_conversation_not_found(app, db):
    with app.app_context():
        result = get_conversation(1, 2)
        assert result is None

def test_create_conversation(app, db):
    with app.app_context():
        user1, user2 = _create_users(db)
        conv = create_conversation(user1.id, user2.id)
        assert conv.id is not None
        assert conv.user1_id == user1.id
        assert conv.user2_id == user2.id

def test_get_messages(app, db):
    with app.app_context():
        user1, user2 = _create_users(db)
        conv = Conversations(user1_id=user1.id, user2_id=user2.id)
        db.session.add(conv)
        db.session.commit()
        msg = Messages(conversation_id=conv.id, sender_id=user1.id, content="hello")
        db.session.add(msg)
        db.session.commit()
        messages = get_messages(conv.id)
        assert len(messages) == 1
        assert messages[0].content == "hello"

def test_create_message(app, db):
    with app.app_context():
        user1, user2 = _create_users(db)
        conv = Conversations(user1_id=user1.id, user2_id=user2.id)
        db.session.add(conv)
        db.session.commit()
        msg = create_message(conv.id, user1.id, "new message")
        assert msg.id is not None
        assert msg.content == "new message"

def test_get_user_conversations(app, db):
    with app.app_context():
        user1, user2 = _create_users(db)
        conv = Conversations(user1_id=user1.id, user2_id=user2.id)
        db.session.add(conv)
        db.session.commit()
        convs = get_user_conversations(user1.id)
        assert len(convs) == 1
        assert convs[0].id == conv.id

def test_mark_messages_read(app, db):
    with app.app_context():
        user1, user2 = _create_users(db)
        conv = Conversations(user1_id=user1.id, user2_id=user2.id)
        db.session.add(conv)
        db.session.commit()
        msg = Messages(conversation_id=conv.id, sender_id=user1.id, content="hello")
        db.session.add(msg)
        db.session.commit()
        mark_messages_read(conv.id, user2.id)
        updated_msg = Messages.query.get(msg.id)
        assert updated_msg.read_at is not None
