import unittest
from test_helpers import (create_user,
                          delete_user,
                          create_chat,
                          delete_chat,
                          create_message,
                          delete_message,
                          update_message,
                          get_all_message,
                          like_message)


endpoint = "http://127.0.0.1:8002"


class Test_message_endpoints(unittest.TestCase):

    def test_create_messages(self):
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

        # Create new chat
        chat_data = {"chat_name": "Close friends",
                     "chat_passkey": "1234",
                     "users": [user1["id"]]}
        chat = create_chat(chat_data, user2["header"])

        # User1 sends a message
        message_data = {"message": "Testing my message route!"}
        create_message(chat['id'], user1["header"], message_data)

        # Delete the chat and users
        delete_chat(chat['id'], user2["header"], chat_data)
        delete_user(data2, user2["header"])
        delete_user(data1, user1["header"])

    def test_create_messages_error(self):
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

        # Create new chat
        chat_data = {"chat_name": "Close friends",
                     "chat_passkey": "1234",
                     "users": [user1["id"]]}
        chat = create_chat(chat_data, user2["header"])

        # User1 sends a message
        message_data = {"message": "Testing my message route!"}
        create_message(chat['id'], user1["header"], message_data)

        # Delete the chat and users
        delete_chat(chat['id'], user2["header"], chat_data)
        delete_user(data2, user2["header"])
        delete_user(data1, user1["header"])

    def test_delete_messages(self):
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

        # Create new chat
        chat_data = {"chat_name": "Close friends",
                     "chat_passkey": "1234",
                     "users": [user1["id"]]}
        chat = create_chat(chat_data, user2["header"])

        # User1 sends a message
        message_data = {"message": "Testing my message route!"}
        message_response = create_message(chat['id'],
                                          user1["header"],
                                          message_data)

        # Delete message
        delete_message(message_response["id"], user1["header"], message_data)

        # Delete the chat and users
        delete_chat(chat['id'], user2["header"], chat_data)
        delete_user(data2, user2["header"])
        delete_user(data1, user1["header"])

    def test_get_chat_messages(self):
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

        # Create new chat
        chat_data = {"chat_name": "Close friends",
                     "chat_passkey": "1234",
                     "users": [user1["id"]]}
        chat = create_chat(chat_data, user2["header"])

        # User1 sends a message
        message_data = {"message": "Testing my message route!"}
        create_message(chat['id'], user1["header"], message_data)

        # Delete the chat and users
        delete_chat(chat['id'], user2["header"], chat_data)
        delete_user(data2, user2["header"])
        delete_user(data1, user1["header"])

    def test_update_message(self):
        # Create first user
        data1 = {"email": "matt@email.com",
                 "username": "Matt",
                 "password": "12345678"}
        user1 = create_user(data1)

        # Create new chat
        chat_data = {"chat_name": "Close friends",
                     "chat_passkey": "1234",
                     "users": []}
        chat = create_chat(chat_data, user1["header"])

        # User1 sends a message
        message_data = {"message": "Testing my message route!"}
        message_response = create_message(
            chat['id'], user1["header"], message_data)

        updated_message_data = {"message": "Just editing my message."}
        update_message(message_response["id"],
                       user1["header"],
                       updated_message_data)

        # Delete message
        delete_message(message_response["id"],
                       user1["header"], updated_message_data)

        # Delete the chat and users
        delete_chat(chat['id'], user1["header"], chat_data)
        delete_user(data1, user1["header"])

    def test_get_all_messages(self):
        # Create first user
        data1 = {"email": "matt@email.com",
                 "username": "Matt",
                 "password": "12345678"}
        user1 = create_user(data1)

        # User1 creates new chat
        chat_data1 = {"chat_name": "Close friends",
                      "chat_passkey": "1234",
                      "users": []}
        chat1 = create_chat(chat_data1, user1["header"])

        # User1 creates second chat
        chat_data2 = {"chat_name": "Second chat",
                      "chat_passkey": "1234",
                      "users": []}
        chat2 = create_chat(chat_data2, user1["header"])

        # User1 sends a message in the first chat
        message_data1 = {"message": "First message!"}
        message_response1 = create_message(chat1['id'],
                                           user1["header"],
                                           message_data1)
        # User1 sends a message in second chat
        message_data2 = {"message": "Second message!"}
        message_response2 = create_message(chat2['id'],
                                           user1["header"],
                                           message_data2)
        # User1 sends a message in first chat
        message_data3 = {"message": "Third message!"}
        message_response3 = create_message(chat1['id'],
                                           user1["header"],
                                           message_data3)

        message_ids = [message_response1["id"],
                       message_response2["id"],
                       message_response3["id"]]

        get_all_message(message_ids, user1["header"])

        # Delete the chats and user
        delete_chat(chat1['id'], user1["header"], chat_data1)
        delete_chat(chat2['id'], user1["header"], chat_data2)
        delete_user(data1, user1["header"])

    def test_like_message(self):
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

        # Create new chat
        chat_data = {"chat_name": "Close friends",
                     "chat_passkey": "1234",
                     "users": [user1["id"]]}
        chat = create_chat(chat_data, user2["header"])

        # User1 sends a message
        message_data = {"message": "Testing my message route!"}
        message_response = create_message(chat['id'],
                                          user1["header"],
                                          message_data)

        # User2 likes message
        like_message(message_response["id"],
                     user2["header"], data2["username"], True)

        # User1 likes message
        like_message(message_response["id"],
                     user1["header"], data1["username"], True)

        # User2 un-likes message
        like_message(message_response["id"],
                     user2["header"], data2["username"], False)

        # Delete the chat and users
        delete_chat(chat['id'], user2["header"], chat_data)
        delete_user(data2, user2["header"])
        delete_user(data1, user1["header"])


if __name__ == "__main__":
    unittest.main()
