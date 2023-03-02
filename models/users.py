from datetime import datetime
from main import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)

    # User's username
    username = db.Column(db.String(20), nullable=False, unique=True)

    # User's password
    password = db.Column(db.String(60), nullable=False)

    # Date user was created
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # Date user was updated
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # Back-relationship with member table, which populates the chats
    # Member table record is deleted when User is deleted
    chats = db.relationship("Member",
                            backref="user",
                            cascade="all, delete")
