from marshmallow.validate import Length
from main import ma


class UserSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "username", "password", "created_at")
    # chats = fields.List(fields.Nested("ChatSchema", only=("name",)))


user_schema = UserSchema()
users_schema = UserSchema(many=True)
