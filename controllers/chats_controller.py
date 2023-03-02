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
        print("this")
        return abort(401, description="Invalid user")

    # Load data from request body into a chat schema
    chat_data = chat_schema.load(request.json)

    print(chat_data)

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

    return jsonify(chat=chat_schema.dump(chat), members_list=member_schema.dump(members))
