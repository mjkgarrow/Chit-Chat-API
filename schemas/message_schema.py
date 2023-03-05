import json
from marshmallow import fields, post_dump
from main import ma


class MessageSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id",
                  "message",
                  "chat_id",
                  "user_id",
                  "created_at",
                  "edited_at",
                  "user",
                  "chat_name")
        load_only = ("chat_id",
                     "user_id",
                     "created_at",
                     "edited_at")

    user = fields.Nested("UserSchema",
                         only=("username",))

    chat_name = fields.Nested("ChatSchema",
                              only=("chat_name",))

    # Code from: https://stackoverflow.com/questions/44162315/convert-object-when-serializing-it
    # Extracts value from nested dict and returns it
    @post_dump(pass_many=True)
    def deserialise_nested_dict(self, data, many):
        # Check if there are many objects deserialised
        if many:
            # Restructure user values to remove nesting
            for d in data:
                if "user" in d.keys():
                    d["user"] = d["user"]["username"]
                if "chat_name" in d.keys():
                    d["chat_name"] = d["chat_name"]["chat_name"]
            # Sort messages by id so they are in chronological order
            data = sorted(data, key=lambda d: d["id"])

        # If only one object deserialised
        else:
            # Restructure user values to remove nesting
            if "user" in data.keys():
                data["user"] = data["user"]["username"]
            if "chat_name" in data.keys():
                data["chat_name"] = data["chat_name"]["chat_name"]

        return data


message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)
