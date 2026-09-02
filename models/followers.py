from datetime import datetime
from config.database import db

class Followers(db.Model):
    __tablename__ = "followers"

    follower_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    following_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, follower_id, following_id):
        self.follower_id = follower_id
        self.following_id = following_id
