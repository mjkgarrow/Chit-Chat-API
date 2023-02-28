from datetime import datetime
from main import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)
    # chats = db.relationship("Member",
    #                         backref="user",
    #                         cascade="all, delete")

    def __repr__(self):
        return f"<User: {self.username}>"
