from marshmallow import fields
from main import ma


class MemberSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ["id",
                  "chat_id",
                  "user_id",
                  "created_at",
                  "member",
                  "chat"]
        load_only = ["chat_id", "user_id",]

    member = fields.Nested("UserSchema",
                           only=("username",))
    chat = fields.Nested("ChatSchema",
                         only=("chat_name",))


member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
