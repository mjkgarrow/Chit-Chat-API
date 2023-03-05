from datetime import timedelta
from flask_jwt_extended import create_access_token
from flask import Blueprint, abort, request, jsonify
from main import db, bcrypt
from models.users import User
from schemas.user_schema import user_schema


auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.post("/signin")
def signin_user():
    """SIGNS IN USER"""

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
