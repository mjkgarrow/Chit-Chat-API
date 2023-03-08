import unittest
import requests
from test_helpers import (create_user,
                          delete_user,
                          create_chat,
                          delete_chat,
                          get_user)


endpoint = "http://127.0.0.1:8002"


class Test_user_endpoints(unittest.TestCase):
    def test_get_users(self):
        response = requests.get(endpoint, timeout=10)
        status_code = response.status_code
        assert status_code == 200

    def test_create_delete_user(self):
        data = {"email": "matt@email.com",
                "username": "Matt",
                "password": "12345678"}

        user = create_user(data)
        delete_user(data, user["header"])

    def test_create_user_incorrect(self):
        data1 = {"email": "matt@email.com",
                 "username": "Matt",
                 "password": "12345678"}

        user = create_user(data1)

        # Create user with incorrect data
        data2 = {"email": "matt@email.com",
                 "password": "12345678"}

        create_user_response1 = requests.post(endpoint + "/users/",
                                              json=data2,
                                              timeout=10)

        assert create_user_response1.status_code == 400

        # Try create user with duplicate data
        data3 = {"email": "matt@email.com",
                 "username": "Matt",
                 "password": "12345678"}

        create_user_response3 = requests.post(endpoint + "/users/",
                                              json=data3,
                                              timeout=10)

        assert create_user_response3.status_code == 400

        delete_user(data1, user["header"])

    def test_update_user(self):
        data = {"email": "matt@email.com",
                "username": "Matt",
                "password": "12345678"}

        user = create_user(data)

        update_data = {"email": "rohan@gmail.com",
                       "username": "Rohan",
                       "password": "87654321"}

        update_user_response = requests.put(endpoint+"/users/",
                                            headers=user["header"],
                                            json=update_data,
                                            timeout=10)

        assert update_user_response.status_code == 200
        assert update_user_response.json()["email"] == update_data["email"]
        assert update_user_response.json(
        )["username"] == update_data["username"]
        assert update_user_response.json(
        )["password_updated"] is True

        update_data2 = {"username": "Matt_New"}

        update_user_response2 = requests.put(endpoint+"/users/",
                                             headers=user["header"],
                                             json=update_data2,
                                             timeout=10)

        assert update_user_response2.status_code == 200
        assert update_user_response2.json()["email"] == update_data["email"]
        assert update_user_response2.json(
        )["username"] == update_data2["username"]
        assert update_user_response2.json(
        )["password_updated"] is False

        delete_user(update_data2, user["header"])

    def test_update_user_incorrect(self):
        data = {"email": "matt@email.com",
                "username": "Matt",
                "password": "12345678"}

        user = create_user(data)

        update_data = {"email": "",
                       "username": "Matt_New",
                       "password": ""}

        update_user_response = requests.put(endpoint+"/users/",
                                            headers=user["header"],
                                            json=update_data,
                                            timeout=10)

        assert update_user_response.status_code == 400
        assert update_user_response.json()[
            "email"] == ["Incorrect email format"]
        assert update_user_response.json()[
            "password"] == ["Incorrect password length, must be between 8 and 20 characters."]

        delete_user(data, user["header"])

    def get_user(self):
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
        chat_data1 = {"chat_name": "Chat 1",
                      "chat_passkey": "",
                      "users": [user1["id"]]}
        chat1 = create_chat(chat_data1, user2["header"])

        # Create second chat
        chat_data2 = {"chat_name": "Chat 2",
                      "chat_passkey": "",
                      "users": [user1["id"]]}
        chat2 = create_chat(chat_data2, user2["header"])

        # Get list of user chats
        get_user(user1["id"], [chat1["id"], chat2["id"]], user1["header"])

        # Delete chats and users
        delete_chat(chat1['id'], user2["header"], chat_data1)
        delete_chat(chat2['id'], user2["header"], chat_data2)
        delete_user(data2, user2["header"])
        delete_user(data1, user1["header"])


if __name__ == "__main__":
    unittest.main()
