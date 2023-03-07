from datetime import timezone, datetime
from marshmallow import fields, pre_dump, post_dump
from main import ma


class MessageSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id",
                  "message",
                  "chat_id",
                  "user_id",
                  "created_at",
                  "user",
                  "chat_name")
        load_only = ("chat_id",
                     "user_id")

    user = fields.Nested("UserSchema",
                         only=("username",))

    chat_name = fields.Nested("ChatSchema",
                              only=("chat_name",))

    # Inspiration from dizzyf:
    # https://stackoverflow.com/questions/44162315/convert-object-when-serializing-it
    # After dump remove nesting and fix datetime string
    @post_dump(pass_many=True)
    def serialise_nested_dict(self, data, many):
        # Check if there are many objects serialised
        if many:
            for d in data:

                if "created_at" in d:
                    d["created_at"] = datetime.fromisoformat(d["created_at"]).replace(
                        tzinfo=timezone.utc).astimezone(tz=None).strftime("%B %d, %Y at %-I:%M:%S %p")

                # Restructure user values to remove nesting
                if "user" in d:
                    d["user"] = d["user"]["username"]

                # Restructure chat_name values to remove nesting
                if "chat_name" in d:
                    d["chat_name"] = d["chat_name"]["chat_name"]

            # Sort messages by id so they are in chronological order
            data = sorted(data, key=lambda d: d["id"])

        # If only one object serialised
        else:
            # Display date in local time
            if "created_at" in data:
                data["created_at"] = datetime.fromisoformat(data["created_at"]).replace(
                    tzinfo=timezone.utc).astimezone(tz=None).strftime("%B %d, %Y at %-I:%M:%S %p")

            # Restructure user values to remove nesting
            if "user" in data:
                data["user"] = data["user"]["username"]

            # Restructure chat_name values to remove nesting
            if "chat_name" in data:
                data["chat_name"] = data["chat_name"]["chat_name"]

        return data


message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)
