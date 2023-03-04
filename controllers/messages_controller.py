from datetime import datetime
from flask_jwt_extended import jwt_required
from flask import Blueprint, abort, request, jsonify
from main import db
from models.chats import Chat
from models.users import User
from models.messages import Message
from schemas.message_schema import message_schema, messages_schema
from helpers import validate_user_chat


messages = Blueprint("messages", __name__, url_prefix="/messages")


@messages.get("/chat/<int:chat_id>")
@jwt_required()
@validate_user_chat
def get_messages(**kwargs):
    """GETS ALL MESSAGES"""

    chat = kwargs["chat"]

    return jsonify(messages_schema.dump(chat.messages))


@messages.post("/chat/<int:chat_id>")
@jwt_required()
@validate_user_chat
def create_message(**kwargs):
    """CREATES MESSAGE ON CHATROOM"""

    user = kwargs["user"]
    chat = kwargs["chat"]

    message_data = message_schema.load(request.json)

    message = Message(chat=chat,
                      user=user,
                      message=message_data["message"])

    db.session.add(message)
    db.session.commit()

    return jsonify(message_schema.dump(message))
