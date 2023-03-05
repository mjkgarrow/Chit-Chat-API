from marshmallow import fields, post_dump
from main import ma
import json


class MessageSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id",
                  "message",
                  "chat_id",
                  "user_id",
                  "created_at",
                  "edited_at",
                  "user")
        load_only = ("chat_id",
                     "user_id",
                     "created_at",
                     "edited_at")

    user = fields.Nested("UserSchema",
                         only=("username",))

    # Code from: https://stackoverflow.com/questions/44162315/convert-object-when-serializing-it
    # Extracts value from nested dict and returns it
    @post_dump(pass_many=True)
    def deserialise_nested_dict(self, data, many):
        # Check if there are many objects deserialised
        if many:
            # Restructure user values to remove nesting
            for d in data:
                d["user"] = d["user"]["username"]

            # Sort messages by id so they are in chronological order
            data = sorted(data, key=lambda d: d["id"])

        # If only one object deserialised
        elif "user" in data.keys():
            # Restructure user values to remove nesting
            data["user"] = data["user"]["username"]

        return data


message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)
