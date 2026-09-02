from datetime import datetime, timedelta
from dao.story_dao import create_story, get_story_view, create_story_view
from service.file_service import save_file

def create_new_story(user_id, file, caption):
    filename = save_file(file, "story", user_id) if file else None
    if not filename:
        return None
    expires_at = datetime.now() + timedelta(hours=24)
    return create_story(user_id, filename, expires_at, caption)

def view_story_by_user(story_id, user_id):
    view = get_story_view(story_id, user_id)
    if not view:
        create_story_view(story_id, user_id)
