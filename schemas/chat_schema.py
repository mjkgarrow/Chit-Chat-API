from datetime import timezone
from marshmallow import fields, post_dump, pre_dump
from main import ma


class ChatSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id",
                  "chat_name",
                  "chat_passkey",
                  "created_at",
                  "users")
        load_only = ("chat_passkey", )

    users = fields.List(fields.Nested("UserSchema",
                                      only=("id", "username",)))

    # Before dump, convert utc time to local time
    @pre_dump
    def convert_utc_datetime_to_local(self, data, **kwargs):
        data.created_at = data.created_at.replace(
            tzinfo=timezone.utc).astimezone(tz=None).strftime("%B %d, %Y")
        return data

    # After dump converts list of user dicts into list of username strings
    @post_dump
    def deserialise_nested_dict(self, data, **kwargs):
        if "users" in data.keys():
            data["users"] = [data["username"] for data in data["users"]]
        return data


chat_schema = ChatSchema()
chats_schema = ChatSchema(many=True)
