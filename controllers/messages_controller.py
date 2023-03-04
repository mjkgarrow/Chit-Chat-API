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


@messages.get("/<int:chat_id>")
@jwt_required()
@validate_user_chat
def get_messages(**kwargs):
    """GETS ALL messages"""

    user = kwargs["user"]
    chat = kwargs["chat"]

    print(chat.messages[0])

    return jsonify(messages_schema.dump(chat.messages))
