from flask import Blueprint, jsonify
from main import db, bcrypt
from models.chats import Chat
from models.users import User
from models.messages import Message

index = Blueprint("index", __name__)


@index.get("/")
def get_index():
    return jsonify(message="Welcome to Chit-Chat, a RESTful API for chatting with friends and creating chatrooms")
