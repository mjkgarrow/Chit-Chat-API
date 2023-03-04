from marshmallow import fields
from main import ma
# from models.users import User


# class UserSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         ordered = True
#         model = User
#         load_only = ["password", "updated_at", "created_at",]

#     chats = fields.List(fields.Nested("ChatSchema",
#                                       only=("chat_name",)))
class UserSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id",
                  "username",
                  "password",
                  "updated_at",
                  "created_at",
                  "chats")
        load_only = ["password", "updated_at", "created_at",]

    chats = fields.List(fields.Nested("ChatSchema",
                                      only=("id", "chat_name",)))


user_schema = UserSchema()
users_schema = UserSchema(many=True)
