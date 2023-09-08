from unittest import TestCase
from test.helper import get_app, logout, purge_db, login, register, register_and_login
import json


class TestLogin(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_normal_run(self):
        register(self.client, "usr")
        data = {
            "login":  "usr",
            "password": "pwd"
        }
        response = self.client.post('/login', json=data)
        self.assertEqual(response.status_code, 200)

    def test_wrong_login(self):
        register(self.client, "usr")
        data = {
            "login":  "wrong_login",
            "password": "pwd"
        }
        response = self.client.post('/login', json=data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, b"Wrong login and/or password")

    def test_wrong_pwd(self):
        register(self.client, 'usr')
        data = {
            "login": "usr",
            "password": "wrong_pwd"
        }
        response = self.client.post('/login', json=data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, b"Wrong login and/or password")

    def test_login_and_logout(self):
        token = register_and_login(self.client, "usr")
        response = self.client.delete(
            '/logout', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Logged out")

    def test_wrong_json_key_login(self):
        register(self.client, 'usr')
        data = {
            "wrong": "usr",
            "password": "wrong_pwd"
        }
        response = self.client.post('/login', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'login'")

    def test_wrong_json_key_password(self):
        register(self.client, 'usr')
        data = {
            "login": "usr",
            "wrong": "wrong_pwd"
        }
        response = self.client.post('/login', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'password'")

    def test_null_json_value_login(self):
        register(self.client, 'usr')
        data = {
            "login": None,
            "password": 'pwd'
        }
        response = self.client.post('/login', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Login must be provided")

    def test_null_json_value_pwd(self):
        register(self.client, 'usr')
        data = {
            "login": 'usr',
            "password": None
        }
        response = self.client.post('/login', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Password must be provided")
