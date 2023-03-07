from datetime import timezone, datetime
from marshmallow import fields, post_dump, pre_dump
from main import ma


class ChatSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id",
                  "chat_name",
                  "chat_passkey",
                  "created_at",
                  "users")
        load_only = ("chat_passkey", )

    users = fields.List(fields.Nested("UserSchema",
                                      only=("id", "username",)))

    # After dump remove nesting and fix datetime string
    @post_dump(pass_many=True)
    def serialise_nested_dict(self, data, many):
        if many:
            for d in data:
                # Display date in local time
                if "created_at" in d:
                    d["created_at"] = datetime.fromisoformat(d["created_at"]).replace(
                        tzinfo=timezone.utc).astimezone(tz=None).strftime("%B %d, %Y at %-I:%M:%S %p")

                # Restructure user values to remove nesting
                if "users" in d.keys():
                    d["users"] = [datum["username"]
                                  for datum in d["users"]]

            # Sort chats by id so they are in chronological order
            data = sorted(data, key=lambda d: d["id"])

        else:
            # Display date in local time
            if "created_at" in data:
                data["created_at"] = datetime.fromisoformat(data["created_at"]).replace(
                    tzinfo=timezone.utc).astimezone(tz=None).strftime("%B %d, %Y at %-I:%M:%S %p")

            # Restructure user values to remove nesting
            if "users" in data.keys():
                data["users"] = [data["username"] for data in data["users"]]
        return data


chat_schema = ChatSchema()
chats_schema = ChatSchema(many=True)
