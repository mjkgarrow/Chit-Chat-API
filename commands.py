from datetime import date
from flask import Blueprint, jsonify
from main import db
from main import bcrypt
from models.users import User
from models.chats import Chat
from models.messages import Message


db_commands = Blueprint("db", __name__)


@db_commands.cli.command("drop")
def drop_tables():
    """DROP TABLES"""
    db.drop_all()
    print("Tables dropped")


@db_commands.cli.command("create")
def create_tables():
    """CREATE TABLES"""
    db.create_all()
    print("Tables created")


@db_commands.cli.command("seed")
def seed_db():
    """SEED TABLES"""

    # Create user instance
    user1 = User(username="Matt",
                 password=bcrypt.generate_password_hash("1234").decode('utf-8'))

    # Create user instance
    user2 = User(username="Beth",
                 password=bcrypt.generate_password_hash("5678").decode('utf-8'))

    # Add users to db and commit
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    # Create chat instance
    chat1 = Chat(chat_name="Chat1",
                 chat_passkey="1234")

    # Create chat instance
    chat2 = Chat(chat_name="Chat2",
                 chat_passkey="1234")

    # Add chats to users
    user1.chats.append(chat1)
    user2.chats.append(chat2)

    # Commit changes to db
    db.session.commit()

    message1 = Message(chat=chat1,
                       user=user1,
                       message="My first message!")
    message2 = Message(chat=chat1,
                       user=user2,
                       message="This is so cool!!!!!")

    db.session.add(message1)
    db.session.add(message2)
    db.session.commit()

    print("Tables seeded")


@db_commands.cli.command("reset")
def reset_db():
    """DROP, CREATE AND SEED TABLES"""

    db.drop_all()
    db.create_all()

    # Create user instance
    user1 = User(username="Matt",
                 password=bcrypt.generate_password_hash("1234").decode('utf-8'))

    # Create user instance
    user2 = User(username="Beth",
                 password=bcrypt.generate_password_hash("5678").decode('utf-8'))

    # Add users to db and commit
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    # Create chat instance
    chat1 = Chat(chat_name="Chat1",
                 chat_passkey="1234")

    # Create chat instance
    chat2 = Chat(chat_name="Chat2",
                 chat_passkey="1234")

    # Add chats to users
    user1.chats.append(chat1)
    user1.chats.append(chat2)
    user2.chats.append(chat1)

    # Commit changes to db
    db.session.commit()

    message1 = Message(chat=chat1,
                       user=user1,
                       message="My first message!")
    message2 = Message(chat=chat1,
                       user=user2,
                       message="This is so cool!!!!!")

    db.session.add(message1)
    db.session.add(message2)
    db.session.commit()

    print("Tables reset")
