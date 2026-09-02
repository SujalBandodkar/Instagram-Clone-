from datetime import datetime, timedelta
from dao.story_dao import (
    get_active_stories, get_story_by_id, create_story, delete_story,
    get_story_view, create_story_view
)
from models import Stories, StoryViews, Users, Roles

def _create_user(db):
    role = Roles(name="user")
    db.session.add(role)
    db.session.commit()
    user = Users(role_id=role.id, username="u1", email="u1@test.com", password_hash="h1")
    db.session.add(user)
    db.session.commit()
    return user

def test_get_active_stories(app, db):
    with app.app_context():
        user = _create_user(db)
        future_time = datetime.now() + timedelta(days=1)
        story = Stories(user_id=user.id, image="img.png", expires_at=future_time, caption="test")
        db.session.add(story)
        db.session.commit()
        stories = get_active_stories([user.id])
        assert len(stories) == 1
        assert stories[0].image == "img.png"

def test_get_story_by_id(app, db):
    with app.app_context():
        user = _create_user(db)
        future_time = datetime.now() + timedelta(days=1)
        story = Stories(user_id=user.id, image="img.png", expires_at=future_time, caption="test")
        db.session.add(story)
        db.session.commit()
        result = get_story_by_id(story.id)
        assert result is not None
        assert result.image == "img.png"

def test_get_story_by_id_not_found(app, db):
    with app.app_context():
        result = get_story_by_id(999)
        assert result is None

def test_create_story(app, db):
    with app.app_context():
        user = _create_user(db)
        future_time = datetime.now() + timedelta(days=1)
        story = create_story(user.id, "new.png", future_time, "caption")
        assert story.id is not None
        assert story.image == "new.png"

def test_delete_story(app, db):
    with app.app_context():
        user = _create_user(db)
        future_time = datetime.now() + timedelta(days=1)
        story = Stories(user_id=user.id, image="img.png", expires_at=future_time, caption="test")
        db.session.add(story)
        db.session.commit()
        delete_story(story)
        result = Stories.query.get(story.id)
        assert result is None

def test_get_story_view(app, db):
    with app.app_context():
        user = _create_user(db)
        future_time = datetime.now() + timedelta(days=1)
        story = Stories(user_id=user.id, image="img.png", expires_at=future_time, caption="test")
        db.session.add(story)
        db.session.commit()
        view = StoryViews(story_id=story.id, user_id=user.id)
        db.session.add(view)
        db.session.commit()
        result = get_story_view(story.id, user.id)
        assert result is not None
        assert result.story_id == story.id

def test_get_story_view_not_found(app, db):
    with app.app_context():
        result = get_story_view(1, 1)
        assert result is None

def test_create_story_view(app, db):
    with app.app_context():
        user = _create_user(db)
        future_time = datetime.now() + timedelta(days=1)
        story = Stories(user_id=user.id, image="img.png", expires_at=future_time, caption="test")
        db.session.add(story)
        db.session.commit()
        view = create_story_view(story.id, user.id)
        assert view.story_id == story.id
        assert view.user_id == user.id
