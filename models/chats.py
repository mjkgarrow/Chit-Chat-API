from datetime import datetime
from main import db


class Chat(db.Model):
    __tablename__ = "chats"
    id = db.Column(db.Integer(), primary_key=True)

    # Name of chatroom
    chat_name = db.Column(db.String(20), nullable=False)

    # Secret passkey for chatroom
    chat_passkey = db.Column(db.String(), nullable=False)

    # Date chatroom was created
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # Back-relationship with the Members table
    members = db.relationship("Member",
                              backref="chat",
                              cascade="all, delete")
