from datetime import datetime
from main import db


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer(), primary_key=True)

    # Message text content
    message = db.Column(db.String(), nullable=False)

    # Member ID of the user that sent the message
    member_id = db.Column(db.Integer(),
                          db.ForeignKey("members.id"),
                          nullable=False)

    # Date message was created
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # Date message was edited
    edited_at = db.Column(db.DateTime(), default=datetime.utcnow)
