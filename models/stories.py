from datetime import datetime
from config.database import db

class Stories(db.Model):
    __tablename__ = "stories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    expires_at = db.Column(db.DateTime, nullable=False)
    views = db.relationship("StoryViews", backref="story", lazy=True, cascade="all, delete-orphan")

    def __init__(self, user_id, image, expires_at, caption=None):
        self.user_id = user_id
        self.image = image
        self.caption = caption
        self.expires_at = expires_at
