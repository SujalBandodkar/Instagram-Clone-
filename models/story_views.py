from datetime import datetime
from config.database import db

class StoryViews(db.Model):
    __tablename__ = "story_views"

    story_id = db.Column(db.Integer, db.ForeignKey("stories.id", ondelete="CASCADE"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    viewed_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, story_id, user_id):
        self.story_id = story_id
        self.user_id = user_id
