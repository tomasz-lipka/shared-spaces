from unittest import TestCase
from test.helper import get_app, logout, purge_db, register, register_and_login


class TestRegistration(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_normal_run(self):
        response = register(self.client, "usr")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"User created")

    def test_registration_pwd_not_same(self):
        data = {
            "login": "usr",
            "password": "pwd",
            "confirm-password": "other_pwd"
        }
        response = self.client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Passwords don\'t match")

    def test_user_already_exists(self):
        register(self.client, "usr")
        response = register(self.client, "usr")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"User already exists")

    def test_wrong_json_key_login(self):
        data = {
            "wrong": "usr",
            "password": "pwd",
            "confirm-password": "other_pwd"
        }
        response = self.client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'login'")

    def test_wrong_json_key_pwd(self):
        data = {
            "login": "usr",
            "wrong": "pwd",
            "confirm-password": "other_pwd"
        }
        response = self.client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'password'")

    def test_wrong_json_key_confirm_pwd(self):
        data = {
            "login": "usr",
            "password": "pwd",
            "wrong": "other_pwd"
        }
        response = self.client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'confirm-password'")

    def test_already_logged_in(self):
        register_and_login(self.client, 'usr')
        response = register(self.client, 'other-usr')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'Already logged in')

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
            "login": "usr",
            "password": None,
            "confirm-password": "other_pwd"
        }
        response = self.client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Password must be provided")

    def test_null_json_value_confirm_pwd(self):
        data = {
            "login": "usr",
            "password": "pwd",
            "confirm-password": None
        }
        response = self.client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Confirm password must be provided")
