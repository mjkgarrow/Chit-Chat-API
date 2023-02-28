from datetime import datetime
from main import db


class Chat(db.Model):
    __tablename__ = "chats"
    id = db.Column(db.Integer(), primary_key=True)
    chat_name = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    members = db.relationship("Member",
                              backref="chat",
                              cascade="all, delete")
