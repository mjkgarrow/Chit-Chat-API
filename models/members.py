from datetime import datetime
from main import db


class Member(db.Model):
    __tablename__ = "members"
    id = db.Column(db.Integer(), primary_key=True)

    # The ID of the chat the user is part of
    chat_id = db.Column(db.Integer(),
                        db.ForeignKey("chats.id"),
                        nullable=False)

    # The ID of the user
    user_id = db.Column(db.Integer(),
                        db.ForeignKey("users.id"),
                        nullable=False)

    # Date added to chat
    added_at = db.Column(db.DateTime(), default=datetime.utcnow)
