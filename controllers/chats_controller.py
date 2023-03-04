from datetime import datetime, timedelta
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token
from flask import Blueprint, abort, request, jsonify
from main import db, bcrypt
from models.chats import Chat
from models.users import User
from schemas.chat_schema import chat_schema, chats_schema


chats = Blueprint("chats", __name__, url_prefix="/chats")


def check_credentials(user, chat, chat_id=-1):
    """Check if user and chat is in db and user is member of chat"""
    if chat_id == -1:
        if not user or chat is None:
            return False
        return True
    else:
        if (not user
            or chat is None
                or chat_id not in [chat.id for chat in user.chats]):
            return False
        return True


@chats.get("/")
def get_chats():
    """GETS ALL CHATS"""

    # Query db for all chats
    chats_list = db.session.execute(db.select(Chat)).scalars()

    # Return JSON of chats
    return jsonify(chats_schema.dump(chats_list))


@chats.get("/<int:chat_id>")
@jwt_required()
def get_chat_secret(chat_id):
    """GETS CHAT SECRET TO GIVE TO OTHER USERS"""

    # Find verified user in db
    user = db.session.get(User, get_jwt_identity())

    # Find chat in db
    chat = db.session.get(Chat, chat_id)

    # Check for correct user/chat credentials
    if not check_credentials(user, chat, chat_id):
        return abort(401, description="Invalid user or chat")

    # Return JSON of chats
    return jsonify(chat_passkey=chat.chat_passkey)


@chats.post("/")
@jwt_required()
def create_chat():
    """CREATES A CHAT AND ADDS CHAT TO USER CHATS LIST"""

    # Find verified user in db
    user = db.session.get(User, get_jwt_identity())

    # If user not in db, return 401
    if not user:
        return abort(401, description="Invalid user")

    # Load data from request body into a chat schema
    chat_data = chat_schema.load(request.json)

    # Create Chat instance, populate with request body data
    chat = Chat(chat_name=chat_data["chat_name"],
                chat_passkey=chat_data["chat_passkey"])

    # Add the chat to the user's list of chats
    user.chats.append(chat)

    # Commit change to db
    db.session.commit()

    return jsonify(chat_schema.dump(chat))


@chats.put("/<int:chat_id>")
@jwt_required()
def update_chat(chat_id):
    """UPDATES A CHAT NAME"""

    # Find verified user in db
    user = db.session.get(User, get_jwt_identity())

    # Find chat in db
    chat = db.session.get(Chat, chat_id)

    # Check for correct user/chat credentials
    if not check_credentials(user, chat, chat_id):
        return abort(401, description="Invalid user or chat")

    # Load data from request body into a chat schema
    chat_data = chat_schema.load(request.json)

    # Create Chat instance, populate with request body data
    chat.chat_name = chat_data["chat_name"]

    # Commit change to db
    db.session.commit()

    return jsonify(chat_schema.dump(chat))


@chats.delete("/<int:chat_id>")
@jwt_required()
def delete_chat(chat_id):
    """UPDATES A CHAT NAME"""

    # Find verified user in db
    user = db.session.get(User, get_jwt_identity())

    # Find chat in db
    chat = db.session.get(Chat, chat_id)

    # Check for correct user/chat credentials
    if not check_credentials(user, chat, chat_id):
        return abort(401, description="Invalid user or chat")

    # Add chat to db
    db.session.delete(chat)
    db.session.commit()

    return jsonify(chat_schema.dump(chat))


@chats.post("/<int:chat_id>")
@jwt_required()
def join_chat(chat_id):
    """UPDATES A CHAT NAME"""

    # Find verified user in db
    user = db.session.get(User, get_jwt_identity())

    # Find chat in db
    chat = db.session.get(Chat, chat_id)

    # Check for correct user/chat credentials
    if not check_credentials(user, chat):
        return abort(401, description="Invalid user or chat")

    # Load user submitted chat secret
    chat_data = chat_schema.load(request.json)

    # Check if user submitted chat secret matches the requested chat secret
    if chat.chat_passkey != chat_data["chat_passkey"]:
        return abort(401, description="Invalid user or passkey")

    # Add chat to user's list
    user.chats.append(chat)

    # Commit change to db
    db.session.commit()

    return jsonify(chat_schema.dump(chat))
