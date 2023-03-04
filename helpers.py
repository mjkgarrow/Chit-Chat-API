from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import abort, request
from main import db
from models.chats import Chat
from models.users import User


def validate_user_chat(f):
    """Inspiration from: https://stackoverflow.com/questions/31141826/how-to-add-arbitrary-kwargs-and-defaults-to-function-using-a-decorator"""
    @wraps(f)
    def decorator(*args, **kwargs):
        # Populate the chat_id variable
        chat_id = kwargs["chat_id"]

        try:
            # Find verified user in db
            user = db.session.get(User, get_jwt_identity())

            # Find chat in db
            chat = db.session.get(Chat, chat_id)

            kwargs["user"] = user
            kwargs["chat"] = chat

        except Exception:
            return abort(401, description="Invalid user or chat")

        if request.method == "POST":
            print(user, chat)
            if not user or chat is None:
                return abort(401, description="Invalid user or chat")
            return f(*args, **kwargs)
        else:
            if (not user
                or chat is None
                    or chat_id not in [chat.id for chat in user.chats]):
                print("3")
                return abort(401, description="Invalid user or chat")
            return f(*args, **kwargs)
    return decorator
