from datetime import datetime
from config.database import db

class Messages(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    read_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, conversation_id, sender_id, content):
        self.conversation_id = conversation_id
        self.sender_id = sender_id
        self.content = content
