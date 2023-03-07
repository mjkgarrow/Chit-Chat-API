import unittest
import requests
import jwt

endpoint = "http://127.0.0.1:8002"


def create_user(data):
    create_user_response = requests.post(endpoint + "/users/",
                                         json=data,
                                         timeout=10)

    assert create_user_response.status_code == 201
    assert "token" in create_user_response.json()

    user_id = jwt.decode(jwt=create_user_response.json()["token"],
                         key='chit chat secret key',
                         algorithms=["HS256"])["sub"]

    token = create_user_response.json()["token"]
    header = {"Authorization": "Bearer " + token}

    get_user_response = requests.get(endpoint + "/users/chats/",
                                     headers=header,
                                     timeout=10)

    assert get_user_response.status_code == 200
    assert get_user_response.json()["username"] == data["username"]

    return {"id": user_id, "header": header}


def delete_user(data, header):
    delete_user_response = requests.delete(endpoint + "/users/",
                                           headers=header,
                                           timeout=10)

    assert delete_user_response.status_code == 200
    assert delete_user_response.json()["username"] == data["username"]


def login_user(data):
    login_user_response = requests.post(endpoint + "/auth/session",
                                        json=data,
                                        timeout=10)

    assert login_user_response.status_code == 200
    assert "token" in login_user_response.json()

    user_id = jwt.decode(jwt=login_user_response.json()["token"],
                         key='chit chat secret key',
                         algorithms=["HS256"])["sub"]

    token = login_user_response.json()["token"]
    header = {"Authorization": "Bearer " + token}

    return {"id": user_id, "header": header}


def create_chat(data, header):
    create_chat_response = requests.post(endpoint + "/chats/",
                                         headers=header,
                                         json=data,
                                         timeout=10)

    # Verify chat was created successfully
    assert create_chat_response.status_code == 201
    assert create_chat_response.json()["chat_name"] == data["chat_name"]

    return {"id": create_chat_response.json()["id"],
            "chat_name": create_chat_response.json()["chat_name"]}


def delete_chat(chat_id, header, data):
    delete_chat_response = requests.delete(endpoint +
                                           f"/chats/{chat_id}",
                                           headers=header,
                                           timeout=10)

    # Verify chat was deleted successfully
    assert delete_chat_response.status_code == 200
    assert delete_chat_response.json()["chat_name"] == data["chat_name"]
    assert delete_chat_response.json()["id"] == chat_id


def update_chat(chat_id, header, data):
    update_chat_response = requests.put(endpoint + f"/chats/{chat_id}",
                                        headers=header,
                                        json=data,
                                        timeout=10)

    assert update_chat_response.status_code == 200
    assert update_chat_response.json(
    )["chat_name"] == data["chat_name"]
    assert update_chat_response.json()["id"] == chat_id


def reset_matt():
    data = {"email": "matt@email.com",
            "username": "Matt",
            "password": "12345678"}
    user = login_user(data)
    delete_user(data, user["header"])


def reset_beth():
    data = {"email": "beth@email.com",
            "username": "Beth",
            "password": "12345678"}
    user = login_user(data)
    delete_user(data, user["header"])


class Test_auth_endpoints(unittest.TestCase):
    def test_login(self):
        data = {"email": "matt@email.com",
                "username": "Matt",
                "password": "12345678"}
        create_user(data)

        user = login_user(data)

        delete_user(data, user["header"])


class Test_user_endpoints(unittest.TestCase):
    def test_get_users(self):
        response = requests.get(endpoint)
        status_code = response.status_code
        assert status_code == 200

    def test_create_delete_user(self):
        data = {"email": "matt@email.com",
                "username": "Matt",
                "password": "12345678"}

        user = create_user(data)
        delete_user(data, user["header"])

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

        delete_user(update_data, user["header"])


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
        # reset_matt()
        # reset_beth()
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
        url = endpoint + f"/chats/{chat['id']}/join"
        join_response = requests.patch(url,
                                       headers=user1["header"],
                                       json=join_data,
                                       timeout=10)

        assert join_response.status_code == 200
        assert join_response.json()["chat_name"] == chat_data["chat_name"]
        assert join_response.json()["id"] == chat["id"]

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
        url = endpoint + f"/chats/{chat['id']}/leave"
        leave_response = requests.patch(url,
                                        headers=user["header"],
                                        timeout=10)

        assert leave_response.status_code == 200
        assert leave_response.json()["chat_name"] == chat_data["chat_name"]
        assert leave_response.json()["id"] == chat["id"]

        # Rejoin chat to delete
        join_data = {"chat_passkey": "1234"}
        url = endpoint + f"/chats/{chat['id']}/join"
        join_response = requests.patch(url,
                                       headers=user["header"],
                                       json=join_data,
                                       timeout=10)

        assert join_response.status_code == 200
        assert join_response.json()["chat_name"] == chat_data["chat_name"]
        assert join_response.json()["id"] == chat["id"]

        # Delete the chat and users
        delete_chat(chat['id'], user["header"], chat_data)
        delete_user(data, user["header"])


class Test_message_endpoints(unittest.TestCase):

    def test_create_messages(self):
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
                     "users": [user1["id"]]}
        chat = create_chat(chat_data, user2["header"])

        # Send chat passkey and join chat
        join_data = {"chat_passkey": "1234"}
        url = endpoint + f"/chats/{chat['id']}/join"
        join_response = requests.patch(url,
                                       headers=user1["header"],
                                       json=join_data,
                                       timeout=10)

        assert join_response.status_code == 200
        assert join_response.json()["chat_name"] == chat_data["chat_name"]
        assert join_response.json()["id"] == chat["id"]

        # Delete the chat and users
        delete_chat(chat['id'], user2["header"], chat_data)
        delete_user(data2, user2["header"])
        delete_user(data1, user1["header"])

    def test_get_chat_messages(self):
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
        url = endpoint + f"/chats/{chat['id']}/join"
        join_response = requests.patch(url,
                                       headers=user1["header"],
                                       json=join_data,
                                       timeout=10)

        assert join_response.status_code == 200
        assert join_response.json()["chat_name"] == chat_data["chat_name"]
        assert join_response.json()["id"] == chat["id"]

        # Delete the chat and users
        delete_chat(chat['id'], user2["header"], chat_data)
        delete_user(data2, user2["header"])
        user1 = login_user(data1)
        delete_user(data1, user1["header"])


if __name__ == "__main__":
    unittest.main()
