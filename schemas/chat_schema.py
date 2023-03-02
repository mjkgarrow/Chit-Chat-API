from marshmallow import fields
from main import ma


class ChatSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ["id",
                  "chat_name",
                  "chat_passkey",
                  "created_at"]
        # load_only = ["password",]

    # messages = fields.List(fields.Nested("MessageSchema", only=("created_date",)))


chat_schema = ChatSchema()
chats_schema = ChatSchema(many=True)
