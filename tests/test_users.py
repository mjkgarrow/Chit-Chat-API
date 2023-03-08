import unittest
import requests
from test_helpers import create_user, delete_user


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


if __name__ == "__main__":
    unittest.main()
