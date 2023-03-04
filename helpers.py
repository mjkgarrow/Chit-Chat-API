from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import abort, request
from main import db
from models.chats import Chat
from models.users import User


def validate_user_chat(f):
    """This decorator authenticates users and chats

    If the decorator is called through a POST route method when
    no chat_id argument is provided then it will only authenticate the user
    and return a user object in the decorated function kwargs.

    If the decorator is called with any other method or provided with
    a chat_id argument it will authenticate the user, 
    verify the chat exists in db, verify the user is a member of chat,
    and return user and chat objects in the decorated function kwargs.

    Parameters
    ----------
    kwargs
        A dict of keyword arguments

    Returns
    -------
    function with kwargs
        kwargs may include a user or chat object, or both


    Inspiration from: https://stackoverflow.com/questions/31141826/how-to-add-arbitrary-kwargs-and-defaults-to-function-using-a-decorator


    """
    @wraps(f)
    def decorator(*args, **kwargs):
        # If function is a POST method and doesn't include a chat_id
        if request.method == "POST" and "chat_id" not in kwargs.keys():
            try:
                # Find verified user in db
                user = db.session.get(User, get_jwt_identity())

                # Initialise user object in kwargs dict
                kwargs["user"] = user

            except Exception:
                return abort(401, description="Invalid user or chat")

            # Return function with new user object included
            return f(*args, **kwargs)

        # If function is requesting verification on user and chat id
        else:
            # Populate the chat_id variable
            chat_id = kwargs["chat_id"]

            try:
                # Find verified user in db
                user = db.session.get(User, get_jwt_identity())

                # Find chat in db
                chat = db.session.get(Chat, chat_id)

                # Initialise user and chat objects in kwargs dict
                kwargs["user"] = user
                kwargs["chat"] = chat

            except Exception:
                return abort(401, description="Invalid user or chat")

            # Verification logic
            if request.method == "POST":
                # If user or chat is not in db, abort
                if not user or chat is None:
                    return abort(401, description="Invalid user or chat")

                # Run decorated func
                return f(*args, **kwargs)
            else:
                # If user or chat is not in db,
                # or user is member of chat, abort
                if (not user
                    or chat is None
                        or chat_id not in [chat.id for chat in user.chats]):
                    return abort(401, description="Invalid user or chat")

                # Run decorated func
                return f(*args, **kwargs)
    return decorator
