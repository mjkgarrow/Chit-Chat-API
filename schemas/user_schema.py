from marshmallow import fields
from main import ma


class UserSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "username")
    # chats = fields.List(fields.Nested("ChatSchema", only=("name",)))


user_schema = UserSchema()
users_schema = UserSchema(many=True)
