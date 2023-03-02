from marshmallow import fields
from main import ma


class MemberSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ["id",
                  "chat_id",
                  "user_id",
                  "created_at"]

    # messages = fields.List(fields.Nested("MessageSchema", only=("created_date",)))


member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
