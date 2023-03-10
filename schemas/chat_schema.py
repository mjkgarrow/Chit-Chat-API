from datetime import datetime
from marshmallow import fields, post_dump
from marshmallow.validate import Length
from main import ma
from helpers import convert_time_to_local


class ChatSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id",
                  "chat_name",
                  "chat_passkey",
                  "created_at",
                  "users")

    # Validate chat name
    chat_name = ma.String(validate=Length(
        min=1, max=20, error="Chat name must be 1 to 20 characters "))

    # Validate passkey
    chat_passkey = ma.String(validate=Length(
        max=20, error="Passkey must be less than 20 characters "))

    users = fields.List(fields.Nested("UserSchema",
                                      only=("id", "username",)))

    # After dump remove nesting and fix datetime string
    @post_dump(pass_many=True)
    def serialise_nested_dict(self, data, many):
        if many:
            for d in data:
                # Display date in local time
                if "created_at" in d:
                    d["created_at"] = convert_time_to_local(
                        datetime.fromisoformat(d["created_at"]))

                # If passkey exists then don't reveal users
                if "chat_passkey" in d and "users" in d:
                    if len(d["chat_passkey"]) > 0:
                        d["users"] = ["Private chat"]
                    else:
                        # Restructure user values to remove nesting
                        d["users"] = [datum["username"]
                                      for datum in d["users"]]

                    d.pop("chat_passkey")

            # Sort chats by id so they are in chronological order
            data = sorted(data, key=lambda d: d["id"])

        else:
            # Display date in local time
            if "created_at" in data:
                data["created_at"] = convert_time_to_local(
                    datetime.fromisoformat(data["created_at"]))

            # If passkey exists then don't reveal users
            if "chat_passkey" in data and "users" in data:
                if len(data["chat_passkey"]) > 0:
                    data["users"] = ["Private chat"]
                else:
                    # Restructure user values to remove nesting
                    data["users"] = [data["username"]
                                     for data in data["users"]]

                data.pop("chat_passkey")

        return data


class ValidateChatSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id",
                  "chat_name",
                  "chat_passkey",
                  "created_at",
                  "users")

    # Validate chat name
    chat_name = ma.String(required=True, validate=Length(
        min=1, max=20, error="Chat name must be 1 to 20 characters."))

    # Validate passkey
    chat_passkey = ma.String(required=True, validate=Length(
        max=20, error="Passkey must be less than 20 characters."))

    users = ma.List(ma.Integer(), required=True)


chat_schema = ChatSchema()
chats_schema = ChatSchema(many=True)

validate_chat_schema = ValidateChatSchema()
