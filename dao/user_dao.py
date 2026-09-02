from config.database import db
from models import Users, Roles, Followers

def get_user_by_id(user_id):
    return Users.query.get(user_id)

def get_user_by_username(username):
    return Users.query.filter_by(username=username).first()

def get_user_by_email(email):
    return Users.query.filter_by(email=email).first()

def get_user_by_username_or_email(username, email):
    return Users.query.filter((Users.username == username) | (Users.email == email)).first()

def create_user(role_id, username, email, password_hash):
    user = Users(role_id, username, email, password_hash)
    db.session.add(user)
    db.session.commit()
    return user

def update_user(user, username, email, bio, profile_picture=None):
    user.username = username
    user.email = email
    user.bio = bio
    if profile_picture:
        user.profile_picture = profile_picture
    db.session.commit()

def get_role_by_name(name):
    return Roles.query.filter_by(name=name).first()

def get_follow(follower_id, following_id):
    return Followers.query.filter_by(follower_id=follower_id, following_id=following_id).first()

def create_follow(follower_id, following_id):
    follow = Followers(follower_id, following_id)
    db.session.add(follow)
    db.session.commit()
    return follow

def delete_follow(follow):
    db.session.delete(follow)
    db.session.commit()

def get_followers_count(user_id):
    return Followers.query.filter_by(following_id=user_id).count()

def get_following_count(user_id):
    return Followers.query.filter_by(follower_id=user_id).count()

def get_following_ids(user_id):
    following = Followers.query.filter_by(follower_id=user_id).all()
    return [follow.following_id for follow in following]

def get_followers(user_id):
    return Users.query.join(
        Followers, Followers.follower_id == Users.id
    ).filter(Followers.following_id == user_id).order_by(Users.username).all()

def get_following(user_id):
    return Users.query.join(
        Followers, Followers.following_id == Users.id
    ).filter(Followers.follower_id == user_id).order_by(Users.username).all()

def get_all_users():
    return Users.query.order_by(Users.created_at.desc()).all()

def search_users(query):
    return Users.query.filter(Users.username.ilike(f"%{query}%")).all()
