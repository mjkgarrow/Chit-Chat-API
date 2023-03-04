from datetime import datetime, timedelta
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token
from flask import Blueprint, abort, request, jsonify
from main import db, bcrypt
from models.users import User
from schemas.user_schema import user_schema


auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.post("/")
def create_user():
    """CREATES USER"""

    # Load data from request body into a user schema
    user_data = user_schema.load(request.json)

    # Check if user already exists
    if db.session.scalars(db.select(User).filter_by(
            username=user_data["username"]).limit(1)).first():
        return abort(400, description="Username already registered")

    # Create a user object to load into db
    user = User(
        username=user_data["username"],
        password=bcrypt.generate_password_hash(
            user_data["password"]).decode("utf-8"))

    # Add and commit user to db
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id),
                                expires_delta=timedelta(days=100))

    return jsonify({"user": user.username, "token": token})


@auth.post("/signin")
def signin_user():
    """CREATES USER"""

    # Load data from request body into a user schema
    user_data = user_schema.load(request.json)

    # Find user in db
    user = db.session.scalars(db.select(User).filter_by(
        username=user_data["username"]).limit(1)).first()

    # Check if user exists and password matches
    if not user or not bcrypt.check_password_hash(user.password,
                                                  user_data["password"]):
        return abort(401, description="Incorrect username or password")

    # Generate new token
    token = create_access_token(identity=str(user.id),
                                expires_delta=timedelta(days=100))

    return jsonify({"user": user.username, "token": token})


@auth.put("/")
@jwt_required()
def update_user():
    """UPDATES USER"""

    # Get current user from db using JWT
    user = db.session.get(User, get_jwt_identity())

    # If user not in db, return error
    if not user:
        return abort(401, description="Invalid user")

    # Load data from request
    user_data = user_schema.load(request.json)

    # Fill out new director object
    user.username = user_data["username"]
    user.password = bcrypt.generate_password_hash(
        user_data["password"]).decode("utf-8")
    user.updated_at = datetime.utcnow()

    # Commit change to db
    db.session.commit()

    return jsonify(user_schema.dump(user))


@auth.delete("/")
@jwt_required()
def delete_user():
    """DELETES USER"""

    # Get current user from db using JWT
    user = db.session.get(User, get_jwt_identity())

    # If user doesn't exist, abort
    if not user:
        return abort(400, description="Username already registered")

    # Delete and commit user to db
    db.session.delete(user)
    db.session.commit()

    return jsonify(user_schema.dump(user))
