from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask import abort, request
from main import db
from models.chats import Chat
from models.users import User
from models.messages import Message


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


    Inspiration from:
    https://stackoverflow.com/questions/31141826/how-to-add-arbitrary-kwargs-and-defaults-to-function-using-a-decorator


    """

    @wraps(f)
    def decorator(*args, **kwargs):
        # Make sure JWT in request - similar to @jwt_required
        verify_jwt_in_request()

        # Find verified user in db
        user = db.session.get(User, get_jwt_identity())

        if user is None:
            return abort(401, description="Invalid user or chat")

        # Initialise user object in kwargs dict
        kwargs["user"] = user

        # Verify chat exists in db
        if "chat_id" in kwargs:
            # Find chat in db
            chat = db.session.get(Chat, kwargs["chat_id"])

            # Verify chat exists
            if chat is None:
                return abort(401, description="Invalid user or chat")

            # check if user is a member of chat
            # Situations that need user to be a member of a chat:
            # - deleting a chat (DELETE)
            # - updating a chat (PUT)
            if request.method == "PUT" or request.method == "DELETE":
                if kwargs["chat_id"] not in [chat.id for chat in user.chats]:
                    return abort(401, description="Invalid user or chat")

            # Initialise chat object in kwargs dict
            kwargs["chat"] = chat

        # Verify message exists in db
        if "message_id" in kwargs:
            message = db.session.get(Message, kwargs["message_id"])

            if message is None:
                return abort(401, description="Invalid user or message")

            # Verify user created message
            if message.user_id == user.id:
                # Initialise message object in kwargs dict
                kwargs["message"] = message

        return f(*args, **kwargs)

    return decorator
