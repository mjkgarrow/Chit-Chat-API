from datetime import timedelta
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token
from flask import Blueprint, abort, request, jsonify
from main import db, bcrypt
from models.users import User
from schemas.user_schema import user_schema, users_schema


users = Blueprint("users", __name__, url_prefix="/users")


@users.get("/")
def get_users():
    users_list = db.session.execute(db.select(User)).scalars()
    return jsonify(users_schema.dump(users_list))


@users.post("/")
def create_user():
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
