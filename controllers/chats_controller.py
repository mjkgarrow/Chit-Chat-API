from flask import Blueprint, abort, jsonify, request
from marshmallow.exceptions import ValidationError
from main import db
from models.chats import Chat
from models.users import User
from schemas.chat_schema import chat_schema, chats_schema, validate_chat_schema
from helpers import validate_user_chat, convert_time_to_local


chats = Blueprint("chats", __name__, url_prefix="/chats")


@chats.get("/")
def get_chats():
    """GETS ALL CHATS"""

    # Query db for all chats
    # Should return a ScalarResult object (using 'scalars'), which is a single item rather than a collection of items, but can be iterated over
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

    # Try load data from request body into a validator chat schema
    try:
        chat_data = validate_chat_schema.load(request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400

    # Create list of users to be added to chat
    users = [kwargs["user"]]
    for user_id in chat_data["users"]:
        # Don't duplicate the current user in the user list
        if user_id == kwargs["user"].id:
            continue

        # If user doesn't exist in db, skip
        # Return an instance based on the given primary key identifier,
        # or None if not found
        user = db.session.get(User, user_id)

        if user is None:
            continue

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

    # Try load data from request body into a chat schema
    try:
        chat_data = chat_schema.load(request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400

    # Create Chat instance, populate with request body data
    if "chat_name" in chat_data:
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

    # Try load data from request body into a chat schema
    try:
        chat_data = chat_schema.load(request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400

    # Check if chatroom is private and passkeys match
    if len(chat.chat_passkey) > 0:
        if ("chat_passkey" not in chat_data) or (chat.chat_passkey != chat_data["chat_passkey"]):
            return abort(401, description="Invalid user or passkey")

    # Add chat to user's list
    user.chats.append(chat)

    # Commit change to db
    db.session.commit()

    response = {"id": chat.id,
                "chat_name": chat.chat_name,
                "created_at": convert_time_to_local(chat.created_at),
                "message_count": len([message.id for message
                                      in chat.messages]),
                "users": [user.username for user in chat.users]}

    # Return JSON of joined chat
    return jsonify(response)


@ chats.patch("/<int:chat_id>/leave")
@ validate_user_chat
def leave_chat(**kwargs):
    """USER LEAVES A CHAT"""

    # Get chat object from decorator
    chat = kwargs["chat"]

    # Get user object from decorator
    user = kwargs["user"]

    # Remove chat from user's chat list
    if chat in user.chats:
        user.chats.remove(chat)

    # If a chat has no members, delete it
    if len(chat.users) == 0:
        db.session.delete(chat)

    # Commit change to db
    db.session.commit()

    # Return JSON of left chat
    return jsonify(chat_schema.dump(chat))
