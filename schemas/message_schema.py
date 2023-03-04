from marshmallow import fields
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
                  "user")
        load_only = ("chat_id",
                     "user_id",
                     "created_at",
                     "edited_at")

    user = fields.Nested("UserSchema",
                         only=("username",))


message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)
