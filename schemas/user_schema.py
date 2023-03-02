from marshmallow import fields
from main import ma


class UserSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ["id",
                  "username",
                  "password",
                  "updated_at",
                  "created_at",
                  "members"]
        load_only = ["password",]

    members = fields.List(fields.Nested("MemberSchema",
                                        only=("chat",)))


user_schema = UserSchema()
users_schema = UserSchema(many=True)
