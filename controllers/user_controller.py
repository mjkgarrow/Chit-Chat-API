from datetime import timedelta
from flask import Blueprint, jsonify, abort, request
from flask_jwt_extended import create_access_token
from marshmallow.exceptions import ValidationError
from main import db, bcrypt
from models.users import User
from schemas.user_schema import user_schema, users_schema, verifyuser_schema
from schemas.message_schema import messages_schema
from helpers import validate_user_chat


users = Blueprint("users", __name__, url_prefix="/users")


@users.get("/")
def get_users():
    """GETS ALL USERS"""

    # Query database for all Users and dump into schema
    users_list = users_schema.dump(
        db.session.execute(db.select(User)).scalars())

    # Remove chats key from user lists as that is private information
    for user in users_list:
        user.pop("chats")

    # Return JSON of all users
    return jsonify(users_list)


@users.post("/")
def create_user():
    """CREATES USER"""

    # Try load data from request body into a user schema
    try:
        user_data = verifyuser_schema.load(request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400

    # Check if user already exists
    if db.session.scalars(db.select(User).filter_by(
            email=user_data["email"]).limit(1)).first():
        return abort(400, description="Email already registered")

    # Create a user object to load into db
    user = User(email=user_data["email"],
                username=user_data["username"],
                password=bcrypt.generate_password_hash(user_data["password"]
                                                       ).decode("utf-8"))

    # Add and commit user to db
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id),
                                expires_delta=timedelta(days=1))

    response = {"token": token,
                "token_type": "Bearer",
                "expires_in": 3600}

    # Return JSON of JWT token info
    return jsonify(response), 201


@users.put("/")
@validate_user_chat
def update_user(**kwargs):
    """UPDATES USER"""

    # Get user object from kwargs
    user = kwargs["user"]

    # Try load data from request body into a user schema
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400

    # Check if provided email is already being used
    if user_data["email"] != user.email:
        users_list = db.session.execute(db.select(User)).scalars()
        if user_data["email"] in [user.email for user in users_list]:
            return abort(401, description="Email already in use")

    user.email = user_data["email"]
    user.username = user_data["username"]
    user.password = bcrypt.generate_password_hash(user_data["password"]
                                                  ).decode("utf-8")

    # Commit change to db
    db.session.commit()

    # Return JSON of updated user
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

    # Return JSON of deleted User
    return jsonify(user_schema.dump(user))


@users.get("/chats/")
@validate_user_chat
def get_user_chats(**kwargs):
    """GETS LIST OF CHATS USER IS MEMBER OF"""

    # Return JSON of user (including list of chats)
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

    # Return JSON of all user's latest messages on all chatrooms
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

    # Return JSON of all messages created by user
    return jsonify(messages_schema.dump(all_messages))
