from datetime import datetime
from config.database import db

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text)
    profile_picture = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    posts = db.relationship("Posts", backref="post_author", lazy=True, cascade="all, delete-orphan")
    comments = db.relationship("Comments", backref="comment_author", lazy=True, cascade="all, delete-orphan")
    likes = db.relationship("Likes", backref="user", lazy=True, cascade="all, delete-orphan")
    stories = db.relationship("Stories", backref="story_author", lazy=True, cascade="all, delete-orphan")
    messages = db.relationship("Messages", backref="sender", lazy=True, cascade="all, delete-orphan")

    def __init__(self, role_id, username, email, password_hash, bio=None, profile_picture=None):
        self.role_id = role_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.bio = bio
        self.profile_picture = profile_picture
