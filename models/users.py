from datetime import datetime
from main import db
from models.members import member_association


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

    # Back-relationship with the Members table
    chats = db.relationship("Chat",
                            secondary=member_association,
                            back_populates="users",
                            cascade="all, delete")

    def __repr__(self):
        return f"<id: {self.id},username: {self.username}>"

    def asdict(self):
        return {"id": self.id,
                "username": self.username,
                "chats": self.chats}
