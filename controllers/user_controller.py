from datetime import datetime, timedelta
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token
from flask import Blueprint, abort, request, jsonify
from main import db, bcrypt
from models.users import User
from schemas.user_schema import user_schema, users_schema


users = Blueprint("users", __name__, url_prefix="/users")


@users.get("/")
def get_users():
    """GETS USERS"""

    # Query database for all Users
    users_list = db.session.execute(db.select(User)).scalars()

    # Return JSON of Users
    return jsonify(users_schema.dump(users_list))


@users.post("/")
def create_user():
    """CREATES USER"""

    # Load data from request body into a user schema
    user_data = user_schema.load(request.json)

    # Check if user already exists
    if db.session.scalars(db.select(User).filter_by(
            username=user_data["username"]).limit(1)).first():
        return abort(400, description="Username already registered")

    # Create a user object to load into database
    user = User(
        username=user_data["username"],
        password=bcrypt.generate_password_hash(
            user_data["password"]).decode("utf-8"))

    # Add and commit user to database
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id), expires_delta=False)

    return jsonify({"user": user.username, "token": token})


@users.post("/signin")
def signin_user():
    """CREATES USER"""

    # Load data from request body into a user schema
    user_data = user_schema.load(request.json)

    # Find user in database
    user = db.session.scalars(db.select(User).filter_by(
        username=user_data["username"]).limit(1)).first()

    # Check if user exists and password matches
    if not user or not bcrypt.check_password_hash(user.password,
                                                  user_data["password"]):
        return abort(401, description="Incorrect username or password")

    # Generate new token
    token = create_access_token(identity=str(user.id), expires_delta=False)

    return jsonify({"user": user.username, "token": token})


@users.put("/")
@jwt_required()
def update_user():
    """UPDATES USER"""

    # Find user in the db
    user = db.session.get(User, get_jwt_identity())

    # If user not in database, return error
    if not user:
        return abort(401, description="Invalid user")

    # Load data from request
    user_data = user_schema.load(request.json)

    # Fill out new director object
    user.username = user_data["username"]
    user.password = bcrypt.generate_password_hash(
        user_data["password"]).decode("utf-8")
    user.updated_at = datetime.utcnow()

    # Add to the database and commit
    db.session.commit()

    return jsonify(user_schema.dump(user))


@users.delete("/")
@jwt_required()
def delete_user():
    """DELETES USER"""

    # Get current user from database using JWT)
    user = db.session.get(User, get_jwt_identity())

    # If user doesn't exist, abort
    if not user:
        return abort(400, description="Username already registered")

    # Delete and commit user to database
    db.session.delete(user)
    db.session.commit()

    return jsonify(user_schema.dump(user))
