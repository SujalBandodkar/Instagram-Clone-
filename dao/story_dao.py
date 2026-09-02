from config.database import db
from models import Stories, StoryViews

def get_active_stories(user_ids):
    from datetime import datetime
    return Stories.query.filter(
        Stories.expires_at > datetime.now(),
        Stories.user_id.in_(user_ids)
    ).order_by(Stories.created_at.desc()).all()

def get_active_stories_by_user(user_id):
    from datetime import datetime
    return Stories.query.filter(
        Stories.expires_at > datetime.now(),
        Stories.user_id == user_id
    ).order_by(Stories.created_at.asc()).all()

def get_story_by_id(story_id):
    return Stories.query.get(story_id)

def create_story(user_id, image, expires_at, caption):
    story = Stories(user_id, image, expires_at, caption)
    db.session.add(story)
    db.session.commit()
    return story

def delete_story(story):
    db.session.delete(story)
    db.session.commit()

def get_story_view(story_id, user_id):
    return StoryViews.query.filter_by(story_id=story_id, user_id=user_id).first()

def create_story_view(story_id, user_id):
    view = StoryViews(story_id, user_id)
    db.session.add(view)
    db.session.commit()
    return view
