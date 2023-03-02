from marshmallow import fields
from main import ma


class UserSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ["id", "username", "password", "updated_at", "created_at"]
        load_only = ["password",]

    # chats = fields.List(fields.Nested("ChatSchema", only=("name",)))


user_schema = UserSchema()
users_schema = UserSchema(many=True)
