from flask import Blueprint, jsonify

index = Blueprint("index", __name__)


@index.get("/")
def get_index():
    return jsonify(message="Welcome to Chit-Chat, a RESTful API \
for chatting with friends, visit https://github.com/mjkgarrow/Chit-Chat-API for endpoint documentation")
