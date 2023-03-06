from marshmallow import fields
from main import ma


class UserSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id",
                  "username",
                  "password",
                  "created_at",
                  "chats")
        load_only = ["password", "created_at",]

    chats = fields.List(fields.Nested("ChatSchema",
                                      only=("id", "chat_name",)))


user_schema = UserSchema()
users_schema = UserSchema(many=True)
