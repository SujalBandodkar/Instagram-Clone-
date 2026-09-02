from config.database import db
from models import Posts, Comments, Likes
from sqlalchemy import func

def get_posts_by_user_ids(user_ids):
    return Posts.query.filter(Posts.user_id.in_(user_ids)).order_by(Posts.created_at.desc()).all()

def get_posts_by_user_ids_paginated(user_ids, page, per_page, seed):
    return Posts.query.filter(
        Posts.user_id.in_(user_ids)
    ).order_by(func.rand(seed)).limit(per_page).offset((page - 1) * per_page).all()

def get_post_by_id(post_id):
    return Posts.query.get(post_id)

def create_post(user_id, content, image):
    post = Posts(user_id, content, image)
    db.session.add(post)
    db.session.commit()
    return post

def update_post(post, content, image=None):
    if content:
        post.content = content
    if image:
        post.image = image
    db.session.commit()

def delete_post(post):
    db.session.delete(post)
    db.session.commit()

def get_like(user_id, post_id):
    return Likes.query.filter_by(user_id=user_id, post_id=post_id).first()

def create_like(user_id, post_id):
    like = Likes(user_id, post_id)
    db.session.add(like)
    db.session.commit()
    return like

def delete_like(like):
    db.session.delete(like)
    db.session.commit()

def get_user_liked_post_ids(user_id):
    likes = Likes.query.filter_by(user_id=user_id).all()
    return [like.post_id for like in likes]

def get_comment_by_id(comment_id):
    return Comments.query.get(comment_id)

def create_comment(post_id, user_id, content):
    comment = Comments(post_id, user_id, content)
    db.session.add(comment)
    db.session.commit()
    return comment

def delete_comment(comment):
    db.session.delete(comment)
    db.session.commit()

def get_all_posts():
    return Posts.query.order_by(Posts.created_at.desc()).all()

def search_posts(query):
    return Posts.query.filter(Posts.content.ilike(f"%{query}%")).all()
