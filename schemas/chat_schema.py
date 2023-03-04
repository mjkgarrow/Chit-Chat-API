from marshmallow import fields
from main import ma


class ChatSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id",
                  "chat_name",
                  "chat_passkey",
                  "created_at",
                  "users")
        load_only = ("chat_passkey", "created_at")

    users = fields.List(fields.Nested("UserSchema",
                                      only=("id", "username",)))


chat_schema = ChatSchema()
chats_schema = ChatSchema(many=True)
