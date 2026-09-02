from dao.user_dao import get_following_ids
from dao.post_dao import (
    get_posts_by_user_ids, get_posts_by_user_ids_paginated, get_user_liked_post_ids, create_post,
    update_post, get_like, delete_like, create_like,
    create_comment, get_comment_by_id, get_post_by_id, delete_comment
)
from dao.story_dao import get_active_stories
from service.file_service import save_file

def get_home_feed(user_id):
    following_ids = get_following_ids(user_id)
    following_ids.append(user_id)
    
    posts = get_posts_by_user_ids(following_ids)
    stories = get_active_stories(following_ids)
    liked_post_ids = get_user_liked_post_ids(user_id)
    
    return posts, stories, liked_post_ids

def get_home_feed_page(user_id, page, per_page, seed):
    following_ids = get_following_ids(user_id)
    following_ids.append(user_id)

    posts = get_posts_by_user_ids_paginated(following_ids, page, per_page, seed)
    liked_post_ids = get_user_liked_post_ids(user_id)

    return posts, liked_post_ids

def create_new_post(user_id, content, file):
    filename = save_file(file, "post", user_id) if file else None
    post = create_post(user_id, content, filename)
    return post

def update_existing_post(post, content, file):
    filename = save_file(file, "post", post.user_id) if file else None
    update_post(post, content, filename)
    return post

def toggle_like(user_id, post_id):
    like = get_like(user_id, post_id)
    if like:
        delete_like(like)
        return False
    else:
        create_like(user_id, post_id)
        return True

def add_new_comment(post_id, user_id, content):
    return create_comment(post_id, user_id, content)

def remove_comment(comment_id, user_id):
    comment = get_comment_by_id(comment_id)
    if not comment:
        return False
    if comment.user_id != user_id:
        post = get_post_by_id(comment.post_id)
        if not post or post.user_id != user_id:
            return False
    delete_comment(comment)
    return True
