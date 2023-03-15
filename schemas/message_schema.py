from datetime import datetime
from marshmallow import validate, post_dump
from main import ma
from helpers import convert_time_to_local


class MessageSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id",
                  "message",
                  "chat_id",
                  "user_id",
                  "created_at",
                  "user",
                  "chat_name",
                  "likes")
        load_only = ("chat_id",
                     "user_id")

    # Validate message is present and correct length
    message = ma.String(required=True,
                        validate=[
                            validate.Length(min=1,
                                            error="Message empty"),
                            validate.Length(min=1,
                                            max=5000,
                                            error="Message too long, \
                                                must be under 5000 characters")])

    user = ma.Nested("UserSchema",
                     only=("username",))

    likes = ma.List(ma.Nested("UserSchema",
                              only=("username",)))

    chat_name = ma.Nested("ChatSchema",
                          only=("chat_name",))

    # Inspiration from dizzyf:
    # https://stackoverflow.com/questions/44162315/convert-object-when-serializing-it
    # After dump remove nesting and fix datetime string
    @post_dump(pass_many=True)
    def serialise_nested_dict(self, data, many):
        # Check if there are many objects serialised
        if many:
            for d in data:
                # Display date in local time
                if "created_at" in d:
                    d["created_at"] = convert_time_to_local(
                        datetime.fromisoformat(d["created_at"]))

                # Restructure user values to remove nesting
                if "user" in d:
                    d["user"] = d["user"]["username"]

                # Restructure chat_name values to remove nesting
                if "chat_name" in d:
                    d["chat_name"] = d["chat_name"]["chat_name"]

                # Tally likes and list users who liked
                if len(d["likes"]) > 0:
                    d["likes"] = {"count": len(d["likes"]),
                                  "users": [like["username"] for like in d["likes"]]}
                else:
                    d["likes"] = {"count": 0,
                                  "users": []}

            # Sort messages by id so they are in chronological order
            data = sorted(data, key=lambda d: d["id"])

        # If only one object serialised
        else:
            # Display date in local time
            if "created_at" in data:
                data["created_at"] = convert_time_to_local(
                    datetime.fromisoformat(data["created_at"]))

            # Restructure user values to remove nesting
            if "user" in data:
                data["user"] = data["user"]["username"]

            # Restructure chat_name values to remove nesting
            if "chat_name" in data:
                data["chat_name"] = data["chat_name"]["chat_name"]

            # Tally likes and list users who liked
            if len(data["likes"]) > 0:
                data["likes"] = {"count": len(data["likes"]),
                                 "users": [like["username"] for
                                           like in data["likes"]]}
            else:
                data["likes"] = {"count": 0,
                                 "users": []}

        return data


message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)
