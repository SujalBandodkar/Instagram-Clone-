import pytest
from flask import Flask
from config.database import db as _db

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = True
    _db.init_app(app)
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture
def db(app):
    return _db

@pytest.fixture
def client(app):
    return app.test_client()
