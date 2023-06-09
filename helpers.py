from datetime import timezone
from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask import abort, request
from main import db
from models.chats import Chat
from models.users import User
from models.messages import Message


def validate_user_chat(f):
    """This decorator authenticates users, chats and messages

    Parameters
    ----------
    kwargs
        A dict of keyword arguments

    Returns
    -------
    function with kwargs
        kwargs include a user object and possibly a chat or message object, or all three


    Inspiration from:
    https://stackoverflow.com/questions/31141826/how-to-add-arbitrary-kwargs-and-defaults-to-function-using-a-decorator


    """

    @wraps(f)
    def decorator(*args, **kwargs):
        # Make sure JWT in request - similar to @jwt_required
        verify_jwt_in_request()

        # Find verified user in db
        # Return an instance based on the given primary key identifier,
        # or None if not found
        user = db.session.get(User, get_jwt_identity())

        # If user can't be found return a 401 error,
        # keep message information secure so malicious actor can't use it
        if user is None:
            return abort(401, description="Invalid user or chat")

        # Initialise user object in kwargs dict
        kwargs["user"] = user

        # Verify chat exists in db
        if "chat_id" in kwargs:
            # Find chat in db
            # Return an instance based on the given primary key identifier,
            # or None if not found
            chat = db.session.get(Chat, kwargs["chat_id"])

            # If chat can't be found return a 401 error
            if chat is None:
                return abort(401, description="Invalid user or chat")

            # Check if user is a member of chat
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
            # Find the message in the db
            # Return an instance based on the given primary key identifier,
            # or None if not found
            message = db.session.get(Message, kwargs["message_id"])

            # If message can't be found return a 401 error
            if message is None:
                return abort(401, description="Invalid user or message")

            # Check user created message, if not then unauthorised
            if message.user_id == user.id:
                kwargs["message"] = message
            else:
                return abort(401, description="You can only edit your own messages.")

        return f(*args, **kwargs)

    return decorator


def convert_time_to_local(date):
    """Convert a UTC datetime object to a local time string"""
    return date.replace(tzinfo=timezone.utc
                        ).astimezone(tz=None
                                     ).strftime("%B %d, %Y at %-I:%M:%S %p")
