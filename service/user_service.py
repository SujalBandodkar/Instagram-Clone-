import bcrypt
from dao.user_dao import (
    get_user_by_username_or_email, get_role_by_name, create_user,
    get_user_by_username, get_user_by_email, get_user_by_id, get_followers_count,
    get_following_count, get_follow, update_user, search_users,
    delete_follow, create_follow, get_followers, get_following
)
from dao.post_dao import get_posts_by_user_ids, search_posts
from service.file_service import save_file

def register_user(username, email, password):
    existing_user = get_user_by_username_or_email(username, email)
    if existing_user:
        return {"error": "Username or email already exists"}, 409

    user_role = get_role_by_name("user")
    if user_role is None:
        return {"error": "User role not configured"}, 500

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user = create_user(user_role.id, username, email, password_hash)
    return {"user": user}, 201

def login_user(email, password):
    user = get_user_by_email(email)
    if user is None:
        return None
    if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
        return None
    return user

def get_profile_data(user_id, current_user_id):
    user = get_user_by_id(user_id)
    if user is None:
        return None
    
    posts = get_posts_by_user_ids([user_id])
    followers_count = get_followers_count(user_id)
    following_count = get_following_count(user_id)
    is_following = get_follow(current_user_id, user_id) is not None
    
    return {
        "user": user,
        "posts": posts,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following
    }

def update_profile(user_id, username, email, bio, file):
    user = get_user_by_id(user_id)
    if user is None:
        return {"error": "User not found"}, 404
    existing_username = get_user_by_username(username)
    if existing_username and existing_username.id != user_id:
        return {"error": "Username already exists"}, 409
        
    existing_email = get_user_by_username_or_email(None, email)
    if existing_email and existing_email.id != user_id:
        return {"error": "Email already exists"}, 409
        
    filename = save_file(file, "profile", user_id) if file else None
    update_user(user, username, email, bio, filename)
    return {"user": user}, 200

def toggle_follow(current_user_id, target_user_id):
    follow = get_follow(current_user_id, target_user_id)
    if follow:
        delete_follow(follow)
        return False
    else:
        create_follow(current_user_id, target_user_id)
        return True

def search_content(query):
    users = search_users(query)
    posts = search_posts(query)
    return users, posts

def get_followers_list(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        return None
    followers = get_followers(user_id)
    return {"user": user, "users": followers, "list_type": "followers"}

def get_following_list(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        return None
    following = get_following(user_id)
    return {"user": user, "users": following, "list_type": "following"}
