from flask import Blueprint, abort, jsonify, request
from marshmallow.exceptions import ValidationError
from main import db
from models.users import User
from models.messages import Message
from schemas.message_schema import message_schema, messages_schema
from helpers import validate_user_chat


messages = Blueprint("messages", __name__, url_prefix="/messages")


@messages.get("/chat/<int:chat_id>")
@validate_user_chat
def get_messages(**kwargs):
    """GETS ALL MESSAGES IN A CHAT"""
    # Get chat object from kwargs
    chat = kwargs["chat"]

    # Return deserialised message objects from chat
    return jsonify(messages_schema.dump(chat.messages))


@messages.post("/chat/<int:chat_id>")
@validate_user_chat
def create_message(**kwargs):
    """CREATES MESSAGE IN A CHAT"""

    # Get user and message objects from kwargs
    user = kwargs["user"]
    chat = kwargs["chat"]

    # Try load data from request body into a message schema
    try:
        message_data = message_schema.load(request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400

    # Create message object
    message = Message(chat=chat,
                      user=user,
                      message=message_data["message"])

    # Add chat name info through backref
    message.chat_name = {"chat_name": chat.chat_name}

    chat.messages.append(message)

    # Add message to db and commit
    db.session.commit()

    # Return deserialised message object
    return jsonify(message_schema.dump(message)), 201


@messages.put("/<int:message_id>")
@validate_user_chat
def update_message(**kwargs):
    """UPDATES A MESSAGE"""

    # Get user and message objects from kwargs
    user = kwargs["user"]
    message = kwargs["message"]

    # Try load data from request body into a message schema
    try:
        message_data = message_schema.load(request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400

    # Verify user created message
    if message.user_id == user.id:
        # Update message content
        message.message = message_data["message"]

    # Commit change to db
    db.session.commit()

    # Return deserialised message object
    return jsonify(message_schema.dump(message))


@messages.delete("/<int:message_id>")
@validate_user_chat
def delete_message(**kwargs):
    """DELETES A MESSAGE"""

    # Check if message object was handed to kwargs
    if "message" in kwargs:
        # Delete message from db
        db.session.delete(kwargs["message"])
        db.session.commit()

        # Return deserialised message object
        return jsonify(message_schema.dump(kwargs["message"]))

    return abort(401, description="Invalid user or message")


@messages.get("/latest_messages/")
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

            # chat_name = chat.chat_name

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
                                    "user": {"username": username},
                                    "sent_at": chat.messages[-1].created_at})

    # Return JSON of all user's latest messages on all chatrooms
    return jsonify(messages_schema.dump(latest_messages))


@messages.get("/all_messages/")
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

    response = messages_schema.dump(all_messages)

    for message in response:
        message.pop("user")

    # Return JSON of all messages created by user
    return jsonify(response)
