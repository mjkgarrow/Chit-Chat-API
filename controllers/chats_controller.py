from datetime import datetime, timedelta
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token
from flask import Blueprint, abort, request, jsonify
from main import db, bcrypt
from models.chats import Chat
from models.users import User
from models.members import Member
from schemas.chat_schema import chat_schema, chats_schema
from schemas.member_schema import member_schema, members_schema


chats = Blueprint("chats", __name__, url_prefix="/chats")


@chats.get("/")
def get_chats():
    """GETS chats"""

    # Query db for all chats
    chats_list = db.session.execute(db.select(Chat)).scalars()

    # Return JSON of chats
    return jsonify(chats_schema.dump(chats_list))


@chats.post("/")
@jwt_required()
def create_chat():
    """CREATES A CHAT WITH MEMBER LIST"""

    # Find verified user in db
    user = db.session.get(User, get_jwt_identity())

    # If user not in db, return error
    if not user:
        return abort(401, description="Invalid user")

    # Load data from request body into a chat schema
    chat_data = chat_schema.load(request.json)

    # Create Chat instance, populate with request body data
    chat = Chat(chat_name=chat_data["chat_name"],
                chat_passkey=chat_data["chat_passkey"])

    # Add chat to db
    db.session.add(chat)
    db.session.commit()

    # Create a Member instance with the chat creator included
    members = Member(chat_id=chat.id,
                     user_id=user.id)

    # Add member to db
    db.session.add(members)
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

    # If user or chat not in db, return error
    if not user or not chat:
        return abort(401, description="Invalid user or chat")

    # Check if user is a member of chat
    chat_member = db.session.execute(
        db.select(Member).filter_by(chat_id=chat.id, user_id=user.id)).scalar()

    if not chat_member:
        return abort(401, description="Invalid user")

    # Load data from request body into a chat schema
    chat_data = chat_schema.load(request.json)

    # Create Chat instance, populate with request body data
    chat.chat_name = chat_data["chat_name"]

    # Add chat to db
    # db.session.add(chat)
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

    # If user or chat not in db, return error
    if not user or not chat:
        return abort(401, description="Invalid user or chat")

    # Check if user is a member of chat
    chat_member = db.session.execute(
        db.select(Member).filter_by(chat_id=chat.id, user_id=user.id)).scalar()

    if not chat_member:
        return abort(401, description="Invalid user")

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

    # If user or chat not in db, return error
    if not user or not chat:
        return abort(401, description="Invalid user or chat")

    # Find member in database
    chat_member = db.session.execute(
        db.select(Member).filter_by(chat_id=chat.id, user_id=user.id)).scalar()

    # If user is a chat member already, then abort
    if chat_member:
        return abort(401, description="Invalid request")

    # Load user submitted chat secret
    chat_data = chat_schema.load(request.json)

    # Check if user submitted chat secret matches the requested chat secret
    if chat.chat_passkey != chat_data["chat_passkey"]:
        return abort(401, description="Invalid user or passkey")

    # Create a new member instance
    member = Member(chat=chat,
                    member=user)

    # Add member to db
    db.session.add(member)
    db.session.commit()

    return jsonify(chat_schema.dump(chat))
