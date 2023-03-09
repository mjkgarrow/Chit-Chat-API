import unittest
from test_helpers import create_user, login_user, delete_user


class Test_auth_endpoints(unittest.TestCase):
    def test_login(self):
        data = {"email": "matt@email.com",
                "username": "Matt",
                "password": "12345678"}
        create_user(data)

        user = login_user(data)

        delete_user(data, user["header"])


if __name__ == "__main__":
    unittest.main()
