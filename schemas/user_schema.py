from marshmallow import validate
from main import ma

email_error = "Incorrect email format."
username_len_error = "Username must be at least 1 character."
username_regex_error = "Username can only contain alphanumeric characters."
pass_len_error = "Incorrect password length, must be between 8 and 20 characters."


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
        error=email_error))

    # Username is a valid length and correct characters
    username = ma.String(validate=[
        validate.Length(min=1,
                        max=20,
                        error=username_len_error),
        validate.Regexp(r'^[a-zA-Z0-9_]+$',
                        error=username_regex_error)])

    # Validate password
    password = ma.String(validate=validate.Length(min=8,
                                                  max=20,
                                                  error=pass_len_error))

    # Displays a list of the user's chats
    chats = ma.List(ma.Nested("ChatSchema"))


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
                      validate=validate.Email(error=email_error))

    # Make sure username is provided, is a valid length and correct characters
    username = ma.String(required=True,
                         validate=[validate.Length(min=1,
                                                   max=20,
                                                   error=username_len_error),
                                   validate.Regexp(r'^[a-zA-Z0-9_]+$',
                                                   error=username_regex_error)])

    # Make sure password is provided and it is a valid length
    password = ma.String(required=True,
                         validate=validate.Length(min=8,
                                                  max=20,
                                                  error=pass_len_error))


user_schema = UserSchema()
users_schema = UserSchema(many=True)

validate_user_schema = ValidateUserSchema()
