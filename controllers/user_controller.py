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
