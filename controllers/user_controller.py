from flask import Blueprint, jsonify, request
from main import db, bcrypt
from models.users import User
from schemas.user_schema import user_schema, users_schema
from schemas.message_schema import messages_schema
from helpers import validate_user_chat


users = Blueprint("users", __name__, url_prefix="/users")


@users.get("/")
def get_users():
    """GETS ALL USERS"""

    # Query database for all Users
    users_list = db.session.execute(db.select(User)).scalars()

    # Return JSON of Users
    return jsonify(users_schema.dump(users_list))


@users.put("/")
@validate_user_chat
def update_user(**kwargs):
    """UPDATES USER"""

    # Get user object from kwargs
    user = kwargs["user"]

    # Load data from request
    user_data = user_schema.load(request.json)

    # Fill out new director object
    user.username = user_data["username"]
    user.password = bcrypt.generate_password_hash(
        user_data["password"]).decode("utf-8")

    # Commit change to db
    db.session.commit()

    return jsonify(user_schema.dump(user))


@users.delete("/")
@validate_user_chat
def delete_user(**kwargs):
    """DELETES USER"""

    # Get user object from kwargs
    user = kwargs["user"]

    # Delete and commit user to db
    db.session.delete(user)
    db.session.commit()

    return jsonify(user_schema.dump(user))


@users.get("/chats/")
@validate_user_chat
def get_user_chats(**kwargs):
    """GETS LIST OF CHATS USER IS MEMBER OF"""

    return jsonify(user_schema.dump(kwargs["user"]))


@users.get("/latest_messages/")
@validate_user_chat
def get_latest_messages(**kwargs):
    """GETS LIST OF LATEST MESSAGES IN USER'S CHATS"""

    user = kwargs["user"]

    # Generate list of latest messages
    latest_messages = []
    for chat in user.chats:
        # Check there are actual messages in the chat
        if chat.messages:

            # Get ID for latest message
            message_id = chat.messages[-1].id

            # Get the chat name
            chat_name = next(found_chat.chat_name for found_chat in user.chats
                             if found_chat.id == chat.messages[-1].chat_id)

            # Get the username of the message creator
            username = db.session.get(User, chat.messages[-1].user_id).username

            # Only append latest messages from other people
            if username == user.username:
                continue

            # Get the message content
            message = chat.messages[-1].message

            # Append all details to latest message
            latest_messages.append({"id": message_id,
                                    "chat_name": {"chat_name": chat_name},
                                    "message": message,
                                    "user": {"username": username}
                                    })

    return jsonify(messages_schema.dump(latest_messages))


@users.get("/all_messages/")
@validate_user_chat
def get_all_messages(**kwargs):
    """GETS LIST OF ALL MESSAGES CREATED BY USER"""

    user = kwargs["user"]

    # Generate list of latest messages
    all_messages = []
    for chat in user.chats:
        # Check there are actual messages in the chat
        if chat.messages:

            # Get all messages created by the user
            for message in chat.messages:
                if message.user_id == user.id:
                    message.chat_name = {"chat_name": chat.chat_name}
                    all_messages.append(message)

    return jsonify(messages_schema.dump(all_messages))
