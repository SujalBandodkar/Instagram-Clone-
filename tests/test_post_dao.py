from dao.post_dao import (
    get_posts_by_user_ids, get_post_by_id, create_post, update_post, delete_post,
    get_like, create_like, delete_like, get_user_liked_post_ids,
    get_comment_by_id, create_comment, delete_comment,
    get_all_posts, search_posts
)
from models import Posts, Comments, Likes, Users, Roles

def _create_user(db):
    role = Roles(name="user")
    db.session.add(role)
    db.session.commit()
    user = Users(role_id=role.id, username="testuser", email="test@test.com", password_hash="hashed")
    db.session.add(user)
    db.session.commit()
    return user

def test_get_posts_by_user_ids(app, db):
    with app.app_context():
        user1 = _create_user(db)
        post = Posts(user_id=user1.id, content="test post", image=None)
        db.session.add(post)
        db.session.commit()
        results = get_posts_by_user_ids([user1.id])
        assert len(results) == 1
        assert results[0].content == "test post"

def test_get_post_by_id(app, db):
    with app.app_context():
        user = _create_user(db)
        post = Posts(user_id=user.id, content="test post", image=None)
        db.session.add(post)
        db.session.commit()
        result = get_post_by_id(post.id)
        assert result is not None
        assert result.content == "test post"

def test_get_post_by_id_not_found(app, db):
    with app.app_context():
        result = get_post_by_id(999)
        assert result is None

def test_create_post(app, db):
    with app.app_context():
        user = _create_user(db)
        post = create_post(user.id, "new post", "img.png")
        assert post.id is not None
        assert post.content == "new post"
        assert post.image == "img.png"

def test_update_post(app, db):
    with app.app_context():
        user = _create_user(db)
        post = Posts(user_id=user.id, content="old content", image="old.png")
        db.session.add(post)
        db.session.commit()
        update_post(post, "new content", "new.png")
        assert post.content == "new content"
        assert post.image == "new.png"

def test_delete_post(app, db):
    with app.app_context():
        user = _create_user(db)
        post = Posts(user_id=user.id, content="delete me", image=None)
        db.session.add(post)
        db.session.commit()
        delete_post(post)
        result = Posts.query.get(post.id)
        assert result is None

def test_get_like(app, db):
    with app.app_context():
        user = _create_user(db)
        post = Posts(user_id=user.id, content="post", image=None)
        db.session.add(post)
        db.session.commit()
        like = Likes(user_id=user.id, post_id=post.id)
        db.session.add(like)
        db.session.commit()
        result = get_like(user.id, post.id)
        assert result is not None
        assert result.user_id == user.id

def test_get_like_not_found(app, db):
    with app.app_context():
        result = get_like(1, 1)
        assert result is None

def test_create_like(app, db):
    with app.app_context():
        user = _create_user(db)
        post = Posts(user_id=user.id, content="post", image=None)
        db.session.add(post)
        db.session.commit()
        like = create_like(user.id, post.id)
        assert like.user_id == user.id
        assert like.post_id == post.id

def test_delete_like(app, db):
    with app.app_context():
        user = _create_user(db)
        post = Posts(user_id=user.id, content="post", image=None)
        db.session.add(post)
        db.session.commit()
        like = Likes(user_id=user.id, post_id=post.id)
        db.session.add(like)
        db.session.commit()
        delete_like(like)
        result = Likes.query.filter_by(user_id=user.id, post_id=post.id).first()
        assert result is None

def test_get_user_liked_post_ids(app, db):
    with app.app_context():
        user = _create_user(db)
        post = Posts(user_id=user.id, content="post", image=None)
        db.session.add(post)
        db.session.commit()
        like = Likes(user_id=user.id, post_id=post.id)
        db.session.add(like)
        db.session.commit()
        ids = get_user_liked_post_ids(user.id)
        assert len(ids) == 1
        assert ids[0] == post.id

def test_get_comment_by_id(app, db):
    with app.app_context():
        user = _create_user(db)
        post = Posts(user_id=user.id, content="post", image=None)
        db.session.add(post)
        db.session.commit()
        comment = Comments(post_id=post.id, user_id=user.id, content="comment")
        db.session.add(comment)
        db.session.commit()
        result = get_comment_by_id(comment.id)
        assert result is not None
        assert result.content == "comment"

def test_get_comment_by_id_not_found(app, db):
    with app.app_context():
        result = get_comment_by_id(999)
        assert result is None

def test_create_comment(app, db):
    with app.app_context():
        user = _create_user(db)
        post = Posts(user_id=user.id, content="post", image=None)
        db.session.add(post)
        db.session.commit()
        comment = create_comment(post.id, user.id, "new comment")
        assert comment.id is not None
        assert comment.content == "new comment"

def test_delete_comment(app, db):
    with app.app_context():
        user = _create_user(db)
        post = Posts(user_id=user.id, content="post", image=None)
        db.session.add(post)
        db.session.commit()
        comment = Comments(post_id=post.id, user_id=user.id, content="comment")
        db.session.add(comment)
        db.session.commit()
        delete_comment(comment)
        result = Comments.query.get(comment.id)
        assert result is None

def test_get_all_posts(app, db):
    with app.app_context():
        user = _create_user(db)
        db.session.add(Posts(user_id=user.id, content="post1", image=None))
        db.session.add(Posts(user_id=user.id, content="post2", image=None))
        db.session.commit()
        posts = get_all_posts()
        assert len(posts) == 2

def test_search_posts(app, db):
    with app.app_context():
        user = _create_user(db)
        db.session.add(Posts(user_id=user.id, content="hello world", image=None))
        db.session.commit()
        results = search_posts("hello")
        assert len(results) == 1
        assert results[0].content == "hello world"
