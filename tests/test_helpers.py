import os
import requests
import jwt
from dotenv import load_dotenv

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
endpoint = "http://127.0.0.1:8002"


def create_user(data):
    create_user_response = requests.post(endpoint + "/users/",
                                         json=data,
                                         timeout=10)

    assert create_user_response.status_code == 201
    assert "token" in create_user_response.json()

    user_id = jwt.decode(jwt=create_user_response.json()["token"],
                         key=secret_key,
                         algorithms=["HS256"])["sub"]

    token = create_user_response.json()["token"]
    header = {"Authorization": "Bearer " + token}

    get_user_response = requests.get(endpoint + f"/users/{user_id}",
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
                         key=secret_key,
                         algorithms=["HS256"])["sub"]

    token = login_user_response.json()["token"]
    header = {"Authorization": "Bearer " + token}

    return {"id": user_id, "header": header}


def get_user(user_id, chat_ids, header):
    get_user_chats_response = requests.get(endpoint + f"/users/{user_id}",
                                           headers=header,
                                           timeout=10)

    # Verify chat was created successfully
    assert get_user_chats_response.status_code == 200
    for chat_id in chat_ids:
        assert chat_id in [chat["id"] for chat
                           in get_user_chats_response.json()]


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


def join_chat(chat_id, header, join_data, chat_data):
    url = endpoint + f"/chats/{chat_id}/join"
    join_response = requests.patch(url,
                                   headers=header,
                                   json=join_data,
                                   timeout=10)

    assert join_response.status_code == 200
    assert join_response.json()["chat_name"] == chat_data["chat_name"]
    assert join_response.json()["id"] == chat_id


def leave_chat(chat_id, header, chat_data):
    url = endpoint + f"/chats/{chat_id}/leave"
    leave_response = requests.patch(url,
                                    headers=header,
                                    timeout=10)

    assert leave_response.status_code == 200
    assert leave_response.json()["chat_name"] == chat_data["chat_name"]
    assert leave_response.json()["id"] == chat_id


def create_message(chat_id, header, message_data):
    url = endpoint + f"/messages/chat/{chat_id}"
    create_message_response = requests.post(url,
                                            json=message_data,
                                            headers=header,
                                            timeout=10)

    assert create_message_response.status_code == 201
    assert create_message_response.json()["message"] == message_data["message"]
    return create_message_response.json()


def update_message(message_id, header, update_message_data):
    url = endpoint + f"/messages/{message_id}"
    update_message_response = requests.put(url,
                                           json=update_message_data,
                                           headers=header,
                                           timeout=10)

    assert update_message_response.status_code == 200
    assert update_message_response.json(
    )["message"] == update_message_data["message"]
    return update_message_response.json()


def delete_message(chat_id, header, message_data):
    url = endpoint + f"/messages/{chat_id}"
    create_message_response = requests.delete(url,
                                              headers=header,
                                              timeout=10)

    assert create_message_response.status_code == 200
    assert create_message_response.json()["id"] == chat_id
    assert create_message_response.json()["message"] == message_data["message"]


def get_chat_message(chat_id, header, message_data, message_id):
    url = endpoint + f"/messages/chat/{chat_id}"
    get_messages_response = requests.get(url,
                                         headers=header,
                                         timeout=10)

    assert get_messages_response.status_code == 200
    assert isinstance(get_messages_response.json(), list)
    if len(get_messages_response.json()) > 0:
        message_ids = [message["id"]
                       for message in get_messages_response.json()]

        message_content = [message["message"]
                           for message in get_messages_response.json()]

        assert message_id in message_ids
        assert message_data["message"] in message_content


def get_all_message(message_ids, header):
    url = endpoint + "/messages/all_messages/"
    get_messages_response = requests.get(url,
                                         headers=header,
                                         timeout=10)

    assert get_messages_response.status_code == 200
    assert isinstance(get_messages_response.json(), list)
    if len(get_messages_response.json()) > 0:
        message_ids_response = [message["id"]
                                for message in get_messages_response.json()]

        for mess_id in message_ids:
            assert mess_id in message_ids_response


def like_message(message_id, header, user_name, liking):
    url = endpoint + f"/messages/like/{message_id}"
    like_messages_response = requests.patch(url,
                                            headers=header,
                                            timeout=10)

    assert like_messages_response.status_code == 200

    if len(like_messages_response.json()["likes"]) == 2:
        if liking:
            assert user_name in like_messages_response.json()["likes"]["users"]
        else:
            assert user_name not in like_messages_response.json()[
                "likes"]["users"]

    return like_messages_response.json()
