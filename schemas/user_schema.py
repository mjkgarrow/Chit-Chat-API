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

    # Validate email
    email = ma.String(validate=Email(
        error="Incorrect email format"))

    # Validate username
    username = ma.String(validate=Length(
        min=1, error="Username must be at least 1 character "))

    # Validate password
    password = ma.String(validate=Length(
        min=8, max=20, error="Incorrect password length, must be between 8 and 20 characters."))

    # Displays a list of the user's chats
    chats = fields.List(fields.Nested("ChatSchema"))


class ValidateUserSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id",
                  "email",
                  "username",
                  "password",
                  "created_at")

    # Make sure email is provided
    email = ma.String(required=True, validate=Email(
        error="Incorrect email format"))

    # Make sure username is provided and it is a valid length
    username = ma.String(required=True, validate=Length(
        min=1, error="Username must be at least 1 character "))

    # Make sure password is provided and it is a valid length
    password = ma.String(required=True, validate=Length(
        min=8, max=20, error="Incorrect password length, must be between 8 and 20 characters."))


user_schema = UserSchema()
users_schema = UserSchema(many=True)

validate_user_schema = ValidateUserSchema()
