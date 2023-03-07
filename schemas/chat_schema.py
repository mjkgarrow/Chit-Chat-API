from datetime import timezone
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

    # Before dump, convert utc time to local time
    @pre_dump
    def convert_utc_to_local(self, data, **kwargs):
        data.created_at = data.created_at.replace(
            tzinfo=timezone.utc).astimezone(tz=None).strftime("%B %d, %Y")
        return data

    # After dump converts list of users dict into list of username strings
    @post_dump(pass_many=True)
    def serialise_nested_dict(self, data, many):
        if many:
            # Restructure user values to remove nesting
            for d in data:
                if "users" in d.keys():
                    d["users"] = [datum["username"]
                                  for datum in d["users"]]
            # Sort chats by id so they are in chronological order
            data = sorted(data, key=lambda d: d["id"])
        else:
            # Restructure user values to remove nesting
            if "users" in data.keys():
                data["users"] = [data["username"] for data in data["users"]]
        return data


chat_schema = ChatSchema()
chats_schema = ChatSchema(many=True)
