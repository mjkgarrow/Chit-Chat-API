from datetime import datetime
from flask_jwt_extended import jwt_required
from flask import Blueprint, abort, request, jsonify
from main import db
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
    """CREATES MESSAGE ON CHATROOM"""

    # Get user and message objects from kwargs
    user = kwargs["user"]
    chat = kwargs["chat"]

    # Load request JSON
    message_data = message_schema.load(request.json)

    # Create message object
    message = Message(chat=chat,
                      user=user,
                      message=message_data["message"])

    chat.messages.append(message)

    # Add message to db and commit
    # db.session.add(message)
    db.session.commit()

    # Return deserialised message object
    return jsonify(message_schema.dump(message))


@messages.put("/<int:message_id>")
@validate_user_chat
def update_message(**kwargs):
    """CREATES MESSAGE ON CHATROOM"""

    # Get user and message objects from kwargs
    user = kwargs["user"]
    message = kwargs["message"]

    # Load request JSON
    message_data = message_schema.load(request.json)

    # Verify user created message
    if message.user_id == user.id:
        # Update message content
        message.message = message_data["message"]

    # Commit change to db
    db.session.commit()

    # Return deserialised message object
    return jsonify(message_schema.dump(message))
