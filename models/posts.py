from datetime import datetime
from config.database import db

class Posts(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = db.Column(db.Text)
    image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    comments = db.relationship("Comments", backref="post", lazy=True, cascade="all, delete-orphan")
    likes = db.relationship("Likes", backref="post", lazy=True, cascade="all, delete-orphan")

    def __init__(self, user_id, content=None, image=None):
        self.user_id = user_id
        self.content = content
        self.image = image
