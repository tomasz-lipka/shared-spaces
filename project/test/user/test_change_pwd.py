from unittest import TestCase
from test.helper import get_app, logout, purge_db, register_and_login


class TestChangePwd(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_not_logged_in(self):
        data = {
            "old-password": "pwd",
            "new-password": "new_pwd",
            "confirm-password": "new_pwd"
        }
        response = self.client.post('/change-password', json=data)
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        register_and_login(self.client, 'usr')
        data = {
            "old-password": "pwd",
            "new-password": "new_pwd",
            "confirm-password": "new_pwd"
        }
        response = self.client.post('/change-password', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Password changed")

        logout(self.client)
        data = {
            "login": 'usr',
            "password": "new_pwd"
        }
        response = self.client.post('/login', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Logged in")

    def test_wrong_old_pwd(self):
        register_and_login(self.client, 'usr')
        data = {
            "old-password": "wrong",
            "new-password": "new_pwd",
            "confirm-password": "new_pwd"
        }
        response = self.client.post('/change-password', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Wrong password")

    def test_wrong_confirmation(self):
        register_and_login(self.client, 'usr')
        data = {
            "old-password": "pwd",
            "new-password": "new_pwd",
            "confirm-password": "wrong_new_pwd"
        }
        response = self.client.post('/change-password', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"New passwords don\'t match")

    def test_wrong_json_key_old_pwd(self):
        register_and_login(self.client, 'usr')
        data = {
            "wrong": "pwd",
            "new-password": "new_pwd",
            "confirm-password": "new_pwd"
        }
        response = self.client.post('/change-password', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'old-password'")

    def test_wrong_json_key_new_pwd(self):
        register_and_login(self.client, 'usr')
        data = {
            "old-password": "pwd",
            "wrong": "new_pwd",
            "confirm-password": "new_pwd"
        }
        response = self.client.post('/change-password', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'new-password'")

    def test_wrong_json_key_confirm_pwd(self):
        register_and_login(self.client, 'usr')
        data = {
            "old-password": "pwd",
            "new-password": "new_pwd",
            "wrong": "new_pwd"
        }
        response = self.client.post('/change-password', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'confirm-password'")
