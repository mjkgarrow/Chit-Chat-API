from marshmallow import fields
from main import ma


class ChatSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ["id",
                  "chat_name",
                  "chat_passkey",
                  "created_at",
                  "members",
                  "messages"]
        load_only = ["chat_passkey",]

    members = fields.List(fields.Nested("MemberSchema",
                                        only=("member",)))
    messages = fields.List(fields.Nested("MessageSchema",
                                         only=("message",
                                               "created_date",)))


chat_schema = ChatSchema()
chats_schema = ChatSchema(many=True)
