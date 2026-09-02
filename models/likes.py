from datetime import datetime
from config.database import db

class Likes(db.Model):
    __tablename__ = "likes"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id
