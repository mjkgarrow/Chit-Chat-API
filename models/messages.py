from datetime import datetime
from main import db
from models.likes import likes_association


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer(), primary_key=True)

    # Message text content
    message = db.Column(db.String(5000), nullable=False)

    # Member ID of the user that sent the message
    chat_id = db.Column(db.Integer(),
                        db.ForeignKey("chats.id"),
                        nullable=False)

    # Member ID of the user that sent the message
    user_id = db.Column(db.Integer(),
                        db.ForeignKey("users.id"),
                        nullable=False)

    # Date message was created
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # The object representation if printed
    def __repr__(self):
        return f"<id: {self.id}, message: {self.message}, user: {self.user_id}>"
