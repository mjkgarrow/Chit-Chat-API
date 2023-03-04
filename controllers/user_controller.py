from datetime import datetime, timedelta
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token
from flask import Blueprint, abort, request, jsonify
from main import db
from models.users import User
from schemas.user_schema import user_schema, users_schema
from schemas.message_schema import message_schema, messages_schema
from helpers import validate_user_chat


users = Blueprint("users", __name__, url_prefix="/users")


@users.get("/")
def get_users():
    """GETS USERS"""

    # Query database for all Users
    users_list = db.session.execute(db.select(User)).scalars()

    # Return JSON of Users
    return jsonify(users_schema.dump(users_list))


@users.get("/chats/")
@jwt_required()
def get_user_chats():
    """GETS LIST OF CHATS USER IS MEMBER OF"""

    # Find user in the db
    user = db.session.get(User, get_jwt_identity())

    # If user not in database
    # or user_id doesn't match current user, return error
    if not user:
        return abort(401, description="Invalid user")

    return jsonify(user_schema.dump(user))


# TODO
@users.get("/messages/")
@jwt_required()
@validate_user_chat
def get_latest_messages(**kwargs):
    """GETS LIST OF CHATS USER IS MEMBER OF"""

    return jsonify(message="TODO")
