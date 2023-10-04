import json
from unittest import TestCase
from test.helper import get_app, logout, purge_db, register, generate_login_from_timestamp


class TestRegistration(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_normal_run(self):
        login = generate_login_from_timestamp()
        data = {
            "login": login,
            "password": "pwd",
            "confirm-password": "pwd"
        }
        response = self.client.post('/register', json=data)
        user = json.loads(response.data.decode('utf-8'))
        self.assertTrue("id" in user)
        self.assertTrue(isinstance(user["id"], int) and user["id"] > 0)
        self.assertEqual(user["login"], login)
        self.assertEqual(response.status_code, 200)

    def test_registration_pwd_not_same(self):
        data = {
            "login": generate_login_from_timestamp(),
            "password": "pwd",
            "confirm-password": "other_pwd"
        }
        response = self.client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Passwords don\'t match")

    def test_user_already_exists(self):
        login = generate_login_from_timestamp()
        data = {
            "login": login,
            "password": "pwd",
            "confirm-password": "pwd"
        }
        self.client.post('/register', json=data)
        data = {
            "login": login,
            "password": "pwd",
            "confirm-password": "pwd"
        }
        response = self.client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"User already exists")

    def test_wrong_json_key_login(self):
        data = {
            "wrong": generate_login_from_timestamp(),
            "password": "pwd",
            "confirm-password": "other_pwd"
        }
        response = self.client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'login'")

    def test_wrong_json_key_pwd(self):
        data = {
            "login": generate_login_from_timestamp(),
            "wrong": "pwd",
            "confirm-password": "other_pwd"
        }
        response = self.client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'password'")

    def test_wrong_json_key_confirm_pwd(self):
        data = {
            "login": generate_login_from_timestamp(),
            "password": "pwd",
            "wrong": "other_pwd"
        }
        response = self.client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'confirm-password'")

    def test_null_json_value_login(self):
        data = {
            "login": None,
            "password": "pwd",
            "confirm-password": "other_pwd"
        }
        response = self.client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Login must be provided")

    def test_null_json_value_pwd(self):
        data = {
            "login": generate_login_from_timestamp(),
            "password": None,
            "confirm-password": "other_pwd"
        }
        response = self.client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Password must be provided")

    def test_null_json_value_confirm_pwd(self):
        data = {
            "login": generate_login_from_timestamp(),
            "password": "pwd",
            "confirm-password": None
        }
        response = self.client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Confirm password must be provided")

    def test_empty_login(self):
        data = {
            "login": "   ",
            "password": "pwd",
            "confirm-password": 'pwd'
        }
        response = self.client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Login cannot be empty")

    def test_min_char_login(self):
        data = {
            "login": "a",
            "password": "pwd",
            "confirm-password": "pwd"
        }
        response = self.client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Login min 3 characters")

    def test_max_char_login(self):
        data = {
            "login": "login login login login login",
            "password": "pwd",
            "confirm-password": "pwd"
        }
        response = self.client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Login max 15 characters")

    def test_empty_pwd(self):
        data = {
            "login": generate_login_from_timestamp(),
            "password": "   ",
            "confirm-password": "pwd"
        }
        response = self.client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Password cannot be empty")

    def test_min_char_pwd(self):
        data = {
            "login": generate_login_from_timestamp(),
            "password": "p",
            "confirm-password": "pwd"
        }
        response = self.client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Password min 3 characters")
