from datetime import datetime
from main import db


class Chat(db.Model):
    __tablename__ = "chats"
    id = db.Column(db.Integer(), primary_key=True)

    # Name of chatroom
    chat_name = db.Column(db.String(20), nullable=False)

    # Date chatroom was created
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # Foreign key of the members list of the chatroom
    members = db.relationship("Member",
                              backref="chat",
                              cascade="all, delete")
