from unittest import TestCase
from test.helper import set_up, client, register, register_and_login


class TestRegistration(TestCase):

    def setUp(self):
        set_up()

    def test_normal_run(self):
        response = register("usr")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"User created")

    def test_registration_pwd_not_same(self):
        data = {
            "login": "usr",
            "password": "pwd",
            "confirm-password": "other_pwd"
        }
        response = client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Passwords don\'t match")

    def test_user_already_exists(self):
        register("usr")
        response = register("usr")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"User already exists")

    def test_wrong_json_key_login(self):
        data = {
            "wrong": "usr",
            "password": "pwd",
            "confirm-password": "other_pwd"
        }
        response = client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'login'")

    def test_wrong_json_key_pwd(self):
        data = {
            "login": "usr",
            "wrong": "pwd",
            "confirm-password": "other_pwd"
        }
        response = client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'password'")

    def test_wrong_json_key_confirm_pwd(self):
        data = {
            "login": "usr",
            "password": "pwd",
            "wrong": "other_pwd"
        }
        response = client.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'confirm-password'")

    def test_already_logged_in(self):
        register_and_login('usr')
        response = register('other-usr')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'Already logged in')
