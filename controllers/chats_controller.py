from flask import Blueprint, abort, jsonify, request
from main import db
from models.chats import Chat
from models.users import User
from schemas.chat_schema import chat_schema, chats_schema
from helpers import validate_user_chat


chats = Blueprint("chats", __name__, url_prefix="/chats")


@chats.get("/")
def get_chats():
    """GETS ALL CHATS"""

    # Query db for all chats
    chats_list = db.session.execute(db.select(Chat)).scalars()

    # Return JSON of chats
    return jsonify(chats_schema.dump(chats_list))


@chats.get("/<int:chat_id>/passkey")
@validate_user_chat
def get_chat_passkey(**kwargs):
    """GETS CHAT SECRET TO GIVE TO OTHER USERS"""

    # Return JSON of chat passkey
    return jsonify(chat_passkey=kwargs["chat"].chat_passkey)


@chats.post("/")
@validate_user_chat
def create_chat(**kwargs):
    """CREATES A CHAT AND ADDS ALL PROVIDED USERS AS MEMBERS"""

    # Load data from request body into a chat schema
    chat_data = chat_schema.load(request.json)

    # Create list of users to be added to chat
    users = [kwargs["user"]]
    for user in chat_data["users"]:
        # Don't duplicate the current user in the user list
        if user["id"] == kwargs["user"].id:
            continue

        # Find verified user in db
        user = db.session.get(User, user["id"])

        if user is None:
            return abort(401, description="Invalid user or chat")

        users.append(user)

    # Create Chat instance, populate with request body data
    chat = Chat(chat_name=chat_data["chat_name"],
                chat_passkey=chat_data["chat_passkey"])

    # Add the chat to the user's list of chats
    for user in users:
        user.chats.append(chat)

    # Commit change to db
    db.session.commit()

    # Return JSON of created chat
    return jsonify(chat_schema.dump(chat)), 201


@chats.put("/<int:chat_id>")
@validate_user_chat
def update_chat(**kwargs):
    """UPDATES A CHAT NAME"""

    chat = kwargs["chat"]

    # Load data from request body into a chat schema
    chat_data = chat_schema.load(request.json)

    # Create Chat instance, populate with request body data
    chat.chat_name = chat_data["chat_name"]

    # Commit change to db
    db.session.commit()

    # Return JSON of updated chat
    return jsonify(chat_schema.dump(chat))


@chats.delete("/<int:chat_id>")
@validate_user_chat
def delete_chat(**kwargs):
    """DELETES A CHAT"""

    # Get chat object from decorator
    chat = kwargs["chat"]

    # Delete chat from db
    db.session.delete(chat)
    db.session.commit()

    # Return JSON of deleted chat
    return jsonify(chat_schema.dump(chat))


@chats.patch("/<int:chat_id>/join")
@validate_user_chat
def join_chat(**kwargs):
    """USER JOINS A CHAT"""

    # Get chat object from decorator
    chat = kwargs["chat"]

    # Get user object from decorator
    user = kwargs["user"]

    # Load user submitted chat secret
    chat_data = chat_schema.load(request.json)

    # Check if user submitted chat secret matches the requested chat secret
    if chat.chat_passkey != chat_data["chat_passkey"]:
        return abort(401, description="Invalid user or passkey")

    # Add chat to user's list
    user.chats.append(chat)

    # Commit change to db
    db.session.commit()

    # Return JSON of joined chat
    return jsonify(chat_schema.dump(chat))


@chats.patch("/<int:chat_id>/leave")
@validate_user_chat
def leave_chat(**kwargs):
    """USER LEAVES A CHAT"""

    # Get chat object from decorator
    chat = kwargs["chat"]

    # Get user object from decorator
    user = kwargs["user"]

    # Remove chat from user's chat list
    if chat in user.chats:
        user.chats.remove(chat)

    # Commit change to db
    db.session.commit()

    # Return JSON of left chat
    return jsonify(chat_schema.dump(chat))
