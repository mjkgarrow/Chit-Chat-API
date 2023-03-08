from datetime import timedelta
from flask import Blueprint, jsonify, abort, request
from flask_jwt_extended import create_access_token
from marshmallow.exceptions import ValidationError
from main import db, bcrypt
from models.users import User
from schemas.user_schema import user_schema, users_schema, validate_user_schema
from helpers import validate_user_chat

users = Blueprint("users", __name__, url_prefix="/users")


@users.get("/")
def get_users():
    """GETS ALL USERS"""

    # Query database for all Users and dump into schema
    users_list = users_schema.dump(
        db.session.execute(db.select(User)).scalars())

    # Remove chats key from user lists as that is private information
    for user in users_list:
        user.pop("chats")

    # Return JSON of all users
    return jsonify(users_list)


@users.post("/")
def create_user():
    """CREATES USER"""

    # Try load data from request body into a user schema
    try:
        user_data = validate_user_schema.load(request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400

    # Check if user already exists
    if db.session.scalars(db.select(User).filter_by(
            email=user_data["email"]).limit(1)).first():
        return abort(400, description="Email already registered")

    # Create a user object to load into db
    user = User(email=user_data["email"],
                username=user_data["username"],
                password=bcrypt.generate_password_hash(user_data["password"]
                                                       ).decode("utf-8"))

    # Add and commit user to db
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id),
                                expires_delta=timedelta(days=1))

    response = {"token": token,
                "token_type": "Bearer",
                "expires_in": 3600}

    # Return JSON of JWT token info
    return jsonify(response), 201


@users.put("/")
@validate_user_chat
def update_user(**kwargs):
    """UPDATES USER"""

    # Get user object from kwargs
    user = kwargs["user"]

    # Try load data from request body into a user schema
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400

    # If an email key was provided, update email
    if "email" in user_data:
        # Check if user is actually providing a different email
        # (to prevent unneccessary db sessions)
        if user_data["email"] != user.email:

            # Check if provided email is already being used
            if db.session.scalars(db.select(User).
                                  filter_by(email=user_data["email"])).first():
                return abort(401, description="Email already in use")

            # Update user's email
            user.email = user_data["email"]

    # If a username key was provided, update username
    if "username" in user_data:
        user.username = user_data["username"]

    # Create response dict to return to user
    response = {"id": user.id,
                "email": user.email,
                "username": user.username,
                "password_updated": False}

    # If a password key was provided, update password
    if "password" in user_data:
        # Check if password is different, to show user the password was updated
        if not bcrypt.check_password_hash(user.password, user_data["password"]):
            response["password_updated"] = True

        user.password = bcrypt.generate_password_hash(user_data["password"]
                                                      ).decode("utf-8")
    # Commit change to db
    db.session.commit()

    # Return JSON of updated user
    return jsonify(response)


@users.delete("/")
@validate_user_chat
def delete_user(**kwargs):
    """DELETES USER"""

    # Get user object from kwargs
    user = kwargs["user"]

    # Delete and commit user to db
    db.session.delete(user)
    db.session.commit()

    # Generate clean list of chats user was member of
    response = user_schema.dump(user)
    response["chats"] = [chat["chat_name"] for chat in response["chats"]]

    # Return JSON of deleted User
    return jsonify(response)


@users.get("/chats/")
@validate_user_chat
def get_user_chats(**kwargs):
    """GETS LIST OF CHATS USER IS MEMBER OF"""

    # Return JSON of user (including list of chats)
    return jsonify(user_schema.dump(kwargs["user"]))
