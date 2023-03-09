import unittest
import requests
from test_helpers import (create_user,
                          delete_user,
                          create_chat,
                          delete_chat,
                          update_chat,
                          join_chat,
                          leave_chat,
                          endpoint)


class Test_chat_endpoints(unittest.TestCase):
    def test_get_chats(self):
        get_chats_response = requests.get(endpoint+"/chats/",
                                          timeout=10)
        assert get_chats_response.status_code == 200

    def test_create_delete_chat(self):
        # Create first user
        data1 = {"email": "matt@email.com",
                 "username": "Matt",
                 "password": "12345678"}

        user1 = create_user(data1)

        # Create second user
        data2 = {"email": "beth@email.com",
                 "username": "Beth",
                 "password": "12345678"}

        user2 = create_user(data2)

        # Create new chat and add first user to it
        chat_data = {"chat_name": "Close friends",
                     "chat_passkey": "",
                     "users": [user1["id"]]}

        chat = create_chat(chat_data, user2["header"])

        delete_chat(chat['id'], user2["header"], chat_data)

        delete_user(data2, user2["header"])

        delete_user(data1, user1["header"])

    def test_update_chat(self):
        # Create first user
        data1 = {"email": "matt@email.com",
                 "username": "Matt",
                 "password": "12345678"}
        user1 = create_user(data1)

        # Create second user
        data2 = {"email": "beth@email.com",
                 "username": "Beth",
                 "password": "12345678"}
        user2 = create_user(data2)

        # Create new chat and add first user to it
        chat_data = {"chat_name": "Close friends",
                     "chat_passkey": "1234",
                     "users": [user1["id"]]}
        chat = create_chat(chat_data, user2["header"])

        # Update the chat
        updated_chat_data = {"chat_name": "New chat name"}
        update_chat(chat['id'], user2["header"], updated_chat_data)

        # Delete the chat and users
        delete_chat(chat['id'], user2["header"], updated_chat_data)
        delete_user(data2, user2["header"])
        delete_user(data1, user1["header"])

    def test_join(self):
        data1 = {"email": "matt@email.com",
                 "username": "Matt",
                 "password": "12345678"}
        user1 = create_user(data1)

        # Create second user
        data2 = {"email": "beth@email.com",
                 "username": "Beth",
                 "password": "12345678"}
        user2 = create_user(data2)

        # Create new chat
        chat_data = {"chat_name": "Close friends",
                     "chat_passkey": "1234",
                     "users": []}
        chat = create_chat(chat_data, user2["header"])

        # Send chat passkey and join chat
        join_data = {"chat_passkey": "1234"}
        join_chat(chat['id'], user1["header"], join_data, chat_data)

        # Delete the chat and users
        delete_chat(chat['id'], user2["header"], chat_data)
        delete_user(data2, user2["header"])
        delete_user(data1, user1["header"])

    def test_leave(self):
        data = {"email": "matt@email.com",
                "username": "Matt",
                "password": "12345678"}
        user = create_user(data)

        # Create new chat
        chat_data = {"chat_name": "Close friends",
                     "chat_passkey": "1234",
                     "users": []}
        chat = create_chat(chat_data, user["header"])

        # Leave chat
        leave_chat(chat['id'], user["header"], chat_data)

        # Rejoin chat to delete
        join_data = {"chat_passkey": "1234"}
        join_chat(chat['id'], user["header"], join_data, chat_data)

        # Delete the chat and users
        delete_chat(chat['id'], user["header"], chat_data)
        delete_user(data, user["header"])


if __name__ == "__main__":
    unittest.main()
