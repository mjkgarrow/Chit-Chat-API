from datetime import datetime
from main import db
from models.members import member_association


class Chat(db.Model, dict):
    __tablename__ = "chats"
    id = db.Column(db.Integer(), primary_key=True)

    # Name of chatroom
    chat_name = db.Column(db.String(20), nullable=False)

    # Secret passkey for chatroom
    chat_passkey = db.Column(db.String(60), nullable=True)

    # Date chatroom was created
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # Relationship with the Users table, back populates
    users = db.relationship("User",
                            secondary=member_association,
                            back_populates="chats")

    def asdict(self):
        return {"id": self.id,
                "chat_name": self.chat_name,
                "users": self.users}

    def __repr__(self):
        return f"<'id': {self.id},'chat_name': {self.chat_name}>"
