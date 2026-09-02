from config.database import db

class Roles(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    users = db.relationship("Users", backref="role", lazy=True)

    def __init__(self, name):
        self.name = name
