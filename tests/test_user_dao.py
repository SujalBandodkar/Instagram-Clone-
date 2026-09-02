from dao.user_dao import (
    get_user_by_id, get_user_by_username, get_user_by_username_or_email,
    create_user, update_user, get_role_by_name, get_follow, create_follow,
    delete_follow, get_followers_count, get_following_count,
    get_following_ids, get_all_users, search_users,
    get_followers, get_following
)
from models import Users, Roles, Followers

def test_get_user_by_id(app, db):
    with app.app_context():
        role = Roles(name="user")
        db.session.add(role)
        db.session.commit()
        user = Users(role_id=role.id, username="testuser", email="test@test.com", password_hash="hashed")
        db.session.add(user)
        db.session.commit()
        result = get_user_by_id(user.id)
        assert result is not None
        assert result.username == "testuser"

def test_get_user_by_id_not_found(app, db):
    with app.app_context():
        result = get_user_by_id(999)
        assert result is None

def test_get_user_by_username(app, db):
    with app.app_context():
        role = Roles(name="user")
        db.session.add(role)
        db.session.commit()
        user = Users(role_id=role.id, username="testuser", email="test@test.com", password_hash="hashed")
        db.session.add(user)
        db.session.commit()
        result = get_user_by_username("testuser")
        assert result is not None
        assert result.username == "testuser"

def test_get_user_by_username_not_found(app, db):
    with app.app_context():
        result = get_user_by_username("nonexistent")
        assert result is None

def test_get_user_by_username_or_email(app, db):
    with app.app_context():
        role = Roles(name="user")
        db.session.add(role)
        db.session.commit()
        user = Users(role_id=role.id, username="testuser", email="test@test.com", password_hash="hashed")
        db.session.add(user)
        db.session.commit()
        result1 = get_user_by_username_or_email("testuser", "other@test.com")
        assert result1 is not None
        result2 = get_user_by_username_or_email("other", "test@test.com")
        assert result2 is not None

def test_get_user_by_username_or_email_not_found(app, db):
    with app.app_context():
        result = get_user_by_username_or_email("nonexistent", "nonexistent@test.com")
        assert result is None

def test_create_user(app, db):
    with app.app_context():
        role = Roles(name="user")
        db.session.add(role)
        db.session.commit()
        user = create_user(role.id, "newuser", "new@test.com", "hashed")
        assert user.id is not None
        assert user.username == "newuser"

def test_update_user(app, db):
    with app.app_context():
        role = Roles(name="user")
        db.session.add(role)
        db.session.commit()
        user = Users(role_id=role.id, username="testuser", email="test@test.com", password_hash="hashed")
        db.session.add(user)
        db.session.commit()
        update_user(user, "updateduser", "updated@test.com", "new bio", "new_pic.png")
        assert user.username == "updateduser"
        assert user.bio == "new bio"
        assert user.profile_picture == "new_pic.png"

def test_get_role_by_name(app, db):
    with app.app_context():
        role = Roles(name="admin")
        db.session.add(role)
        db.session.commit()
        result = get_role_by_name("admin")
        assert result is not None
        assert result.name == "admin"

def test_get_role_by_name_not_found(app, db):
    with app.app_context():
        result = get_role_by_name("nonexistent")
        assert result is None

def test_get_follow(app, db):
    with app.app_context():
        follow = Followers(follower_id=1, following_id=2)
        db.session.add(follow)
        db.session.commit()
        result = get_follow(1, 2)
        assert result is not None
        assert result.follower_id == 1
        assert result.following_id == 2

def test_get_follow_not_found(app, db):
    with app.app_context():
        result = get_follow(1, 2)
        assert result is None

def test_create_follow(app, db):
    with app.app_context():
        follow = create_follow(1, 2)
        assert follow is not None
        assert follow.follower_id == 1
        assert follow.following_id == 2

def test_delete_follow(app, db):
    with app.app_context():
        follow = Followers(follower_id=1, following_id=2)
        db.session.add(follow)
        db.session.commit()
        delete_follow(follow)
        result = Followers.query.filter_by(follower_id=1, following_id=2).first()
        assert result is None

def test_get_followers_count(app, db):
    with app.app_context():
        db.session.add(Followers(follower_id=1, following_id=3))
        db.session.add(Followers(follower_id=2, following_id=3))
        db.session.commit()
        count = get_followers_count(3)
        assert count == 2

def test_get_following_count(app, db):
    with app.app_context():
        db.session.add(Followers(follower_id=1, following_id=2))
        db.session.add(Followers(follower_id=1, following_id=3))
        db.session.commit()
        count = get_following_count(1)
        assert count == 2

def test_get_following_ids(app, db):
    with app.app_context():
        db.session.add(Followers(follower_id=1, following_id=2))
        db.session.add(Followers(follower_id=1, following_id=3))
        db.session.commit()
        ids = get_following_ids(1)
        assert len(ids) == 2
        assert 2 in ids
        assert 3 in ids

def test_get_all_users(app, db):
    with app.app_context():
        role = Roles(name="user")
        db.session.add(role)
        db.session.commit()
        db.session.add(Users(role_id=role.id, username="user1", email="u1@test.com", password_hash="p1"))
        db.session.add(Users(role_id=role.id, username="user2", email="u2@test.com", password_hash="p2"))
        db.session.commit()
        users = get_all_users()
        assert len(users) == 2

def test_search_users(app, db):
    with app.app_context():
        role = Roles(name="user")
        db.session.add(role)
        db.session.commit()
        db.session.add(Users(role_id=role.id, username="john_doe", email="j1@test.com", password_hash="p1"))
        db.session.add(Users(role_id=role.id, username="jane_doe", email="j2@test.com", password_hash="p2"))
        db.session.commit()
        results = search_users("john")
        assert len(results) == 1
        assert results[0].username == "john_doe"

def test_get_followers(app, db):
    with app.app_context():
        role = Roles(name="user")
        db.session.add(role)
        db.session.commit()
        user_a = Users(role_id=role.id, username="alice", email="alice@test.com", password_hash="p1")
        user_b = Users(role_id=role.id, username="bob", email="bob@test.com", password_hash="p2")
        user_c = Users(role_id=role.id, username="charlie", email="charlie@test.com", password_hash="p3")
        db.session.add_all([user_a, user_b, user_c])
        db.session.commit()
        db.session.add(Followers(follower_id=user_a.id, following_id=user_c.id))
        db.session.add(Followers(follower_id=user_b.id, following_id=user_c.id))
        db.session.commit()
        followers = get_followers(user_c.id)
        assert len(followers) == 2
        usernames = {u.username for u in followers}
        assert "alice" in usernames
        assert "bob" in usernames

def test_get_followers_empty(app, db):
    with app.app_context():
        role = Roles(name="user")
        db.session.add(role)
        db.session.commit()
        user = Users(role_id=role.id, username="lonely", email="lonely@test.com", password_hash="p1")
        db.session.add(user)
        db.session.commit()
        followers = get_followers(user.id)
        assert len(followers) == 0

def test_get_following(app, db):
    with app.app_context():
        role = Roles(name="user")
        db.session.add(role)
        db.session.commit()
        user_a = Users(role_id=role.id, username="alice", email="alice@test.com", password_hash="p1")
        user_b = Users(role_id=role.id, username="bob", email="bob@test.com", password_hash="p2")
        user_c = Users(role_id=role.id, username="charlie", email="charlie@test.com", password_hash="p3")
        db.session.add_all([user_a, user_b, user_c])
        db.session.commit()
        db.session.add(Followers(follower_id=user_a.id, following_id=user_b.id))
        db.session.add(Followers(follower_id=user_a.id, following_id=user_c.id))
        db.session.commit()
        following = get_following(user_a.id)
        assert len(following) == 2
        usernames = {u.username for u in following}
        assert "bob" in usernames
        assert "charlie" in usernames

def test_get_following_empty(app, db):
    with app.app_context():
        role = Roles(name="user")
        db.session.add(role)
        db.session.commit()
        user = Users(role_id=role.id, username="lonely", email="lonely@test.com", password_hash="p1")
        db.session.add(user)
        db.session.commit()
        following = get_following(user.id)
        assert len(following) == 0
