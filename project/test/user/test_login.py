from unittest import TestCase
from test.helper import get_app, logout, purge_db, login, register, register_and_login


class TestLogin(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_normal_run(self):
        response = register_and_login(self.client, "usr")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Logged in")

    def test_wrong_login(self):
        response = login(self.client, 'wrong_login')
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
        register_and_login(self.client, "usr")
        response = self.client.get('/logout')
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

    def test_when_already_logged_in(self):
        register_and_login(self.client, 'usr')
        response = login(self.client, 'usr')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, b'Already logged in')

    def test_when_already_logged_in_other_usr(self):
        register(self.client, 'other-usr')
        register_and_login(self.client, 'usr')
        response = login(self.client, 'other-usr')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, b'Already logged in')
