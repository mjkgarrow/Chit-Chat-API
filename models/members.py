from datetime import datetime
from main import db


class Member(db.Model):
    __tablename__ = "members"
    id = db.Column(db.Integer(), primary_key=True)
    chat_id = db.Column(db.Integer(),
                        db.ForeignKey("chats.id"),
                        nullable=False)
    user_id = db.Column(db.Integer(),
                        db.ForeignKey("users.id"),
                        nullable=False)
    chat_creator = db.Column(db.Bool(), default=False)
    added_at = db.Column(db.DateTime(), default=datetime.utcnow)
