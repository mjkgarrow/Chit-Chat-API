import unittest
from test_auth import Test_auth_endpoints
from test_users import Test_user_endpoints
from test_chats import Test_chat_endpoints
from test_messages import Test_message_endpoints


endpoint = "http://127.0.0.1:8002"


if __name__ == "__main__":
    Test_auth_endpoints()
    Test_user_endpoints()
    Test_chat_endpoints()
    Test_message_endpoints()
    unittest.main()
