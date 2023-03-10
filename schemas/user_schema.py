from marshmallow import fields, validate
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
    email = ma.String(validate=validate.Email(
        error="Incorrect email format."))

    # Username is a valid length and correct characters
    username = ma.String(validate=[
        validate.Length(min=1,
                        max=20,
                        error="Username must be at least 1 character."),
        validate.Regexp(r'^[a-zA-Z0-9_]+$',
                        error="Username can only contain alphanumeric characters.")])

    # Validate password
    password = ma.String(validate=validate.Length(min=8,
                                                  max=20,
                                                  error="Incorrect password length, must be between 8 and 20 characters."))

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
    email = ma.String(required=True,
                      validate=validate.Email(error="Incorrect email format"))

    # Make sure username is provided, is a valid length and correct characters
    username = ma.String(required=True,
                         validate=[validate.Length(min=1,
                                                   max=20,
                                                   error="Username must be at least 1 character."),
                                   validate.Regexp(r'^[a-zA-Z0-9_]+$',
                                                   error="Username can only contain alphanumeric characters.")])

    # Make sure password is provided and it is a valid length
    password = ma.String(required=True,
                         validate=validate.Length(min=8,
                                                  max=20,
                                                  error="Incorrect password length, must be between 8 and 20 characters."))


user_schema = UserSchema()
users_schema = UserSchema(many=True)

validate_user_schema = ValidateUserSchema()
