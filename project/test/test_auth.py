from unittest import TestCase
from test.helper import register, login, register_and_login, client, delete_all_records_from_db


class TestAuth(TestCase):

    def setUp(self):
        delete_all_records_from_db()

    def test_registration_pwd_not_same(self):
        data = {
            "login": "usr",
            "password": "pwd",
            "confirm-password": "other_pwd"
        }
        response = client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Passwords don\'t match")

    def test_registration_user_already_exists(self):
        register("usr")
        response = register("usr")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"User already exists")

    def test_proper_registration(self):
        response = register("usr")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"User created")

    def test_wrong_login(self):
        response = login("wrong_login")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, b"Wrong login and/or password")

    def test_wrong_pwd(self):
        register("usr")
        data = {
            "login": "usr",
            "password": "wrong_pwd"
        }
        response = client.post('/login', json=data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, b"Wrong login and/or password")

    def test_login_and_logout(self):
        register_and_login("usr")
        response = client.get('/logout')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Logged out")
