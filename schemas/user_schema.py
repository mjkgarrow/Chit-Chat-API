from marshmallow import fields
from marshmallow.validate import Length, Email
from flask import jsonify
from main import ma


class UserSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id",
                  "email",
                  "username",
                  "password",
                  "created_at",
                  "chats")
        load_only = ["email", "password", "created_at",]

    # Displays a list of the user's chats
    chats = fields.List(fields.Nested("ChatSchema",
                                      only=("id", "chat_name",)))


class VerifyUserSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id",
                  "email",
                  "username",
                  "password",
                  "created_at",
                  "chats")
        load_only = ["email", "password", "created_at",]

    # Make sure email is provided
    email = ma.String(required=True, validate=Email(
        error="Incorrect email format"))

    # Make sure username is provided
    username = ma.String(required=True)

    # Make sure password is provided and it is a valid length
    password = ma.String(required=True, validate=Length(
        min=8, max=20, error="Incorrect password length, must be between 8 and 20 characters."))

    # Displays a list of the user's chats
    chats = fields.List(fields.Nested("ChatSchema",
                                      only=("id", "chat_name",)))


user_schema = UserSchema()
users_schema = UserSchema(many=True)

verifyuser_schema = VerifyUserSchema()
