from flask import Blueprint, jsonify
from main import db
from main import bcrypt
from models.users import User


reset = Blueprint("erase", __name__, url_prefix="/erase")


@reset.get("/")
def reset_server():
    db.drop_all()

    db.create_all()

    user1 = User(username="Matt",
                 password=bcrypt.generate_password_hash("1234").decode('utf-8'))

    user2 = User(username="Beth",
                 password=bcrypt.generate_password_hash("5678").decode('utf-8'))

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    return jsonify(message="Tables dropped, created and seeded")
