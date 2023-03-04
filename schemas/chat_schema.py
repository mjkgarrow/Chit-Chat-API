from marshmallow import fields, post_dump
from main import ma


class ChatSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id",
                  "chat_name",
                  "chat_passkey",
                  "created_at",
                  "updated_at",
                  "users")
        load_only = ("chat_passkey", "updated_at", "created_at")

    users = fields.List(fields.Nested("UserSchema",
                                      only=("id", "username",)))

    # Converts list of user dicts into list of username strings
    @post_dump
    def deserialise_nested_dict(self, data, **kwargs):
        data["users"] = [data["username"] for data in data["users"]]
        return data


chat_schema = ChatSchema()
chats_schema = ChatSchema(many=True)
