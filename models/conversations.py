from datetime import datetime
from config.database import db

class Conversations(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user1_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (db.UniqueConstraint("user1_id", "user2_id"),)

    messages = db.relationship("Messages", backref="conversation", lazy=True, cascade="all, delete-orphan")

    def __init__(self, user1_id, user2_id):
        self.user1_id = user1_id
        self.user2_id = user2_id
