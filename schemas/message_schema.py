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
                  "user")
        load_only = ("chat_id",
                     "user_id",
                     "created_at",
                     "edited_at")

    user = fields.Nested("UserSchema",
                         only=("username",))

    # Code from: https://stackoverflow.com/questions/44162315/convert-object-when-serializing-it
    # Extracts value from nested dict and returns it
    @post_dump
    def deserialise_nested_dict(self, data, **kwargs):
        data['user'] = data['user']["username"]
        return data


message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)
