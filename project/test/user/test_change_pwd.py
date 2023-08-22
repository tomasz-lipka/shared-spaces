from unittest import TestCase
from test.helper import set_up, client, register_and_login, logout


class TestChangePwd(TestCase):

    def setUp(self):
        set_up()

    def test_not_logged_in(self):
        data = {
            "old-password": "pwd",
            "new-password": "new_pwd",
            "confirm-password": "new_pwd"
        }
        response = client.post('/change-password', json=data)
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        register_and_login('usr')
        data = {
            "old-password": "pwd",
            "new-password": "new_pwd",
            "confirm-password": "new_pwd"
        }
        response = client.post('/change-password', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Password changed")

        logout()
        data = {
            "login": 'usr',
            "password": "new_pwd"
        }
        response = client.post('/login', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Logged in")

    def test_wrong_old_pwd(self):
        register_and_login('usr')
        data = {
            "old-password": "wrong",
            "new-password": "new_pwd",
            "confirm-password": "new_pwd"
        }
        response = client.post('/change-password', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Wrong password")

    def test_wrong_confirmation(self):
        register_and_login('usr')
        data = {
            "old-password": "pwd",
            "new-password": "new_pwd",
            "confirm-password": "wrong_new_pwd"
        }
        response = client.post('/change-password', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"New passwords don\'t match")

    def test_wrong_json_key_old_pwd(self):
        register_and_login('usr')
        data = {
            "wrong": "pwd",
            "new-password": "new_pwd",
            "confirm-password": "new_pwd"
        }
        response = client.post('/change-password', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'old-password'")

    def test_wrong_json_key_new_pwd(self):
        register_and_login('usr')
        data = {
            "old-password": "pwd",
            "wrong": "new_pwd",
            "confirm-password": "new_pwd"
        }
        response = client.post('/change-password', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'new-password'")

    def test_wrong_json_key_confirm_pwd(self):
        register_and_login('usr')
        data = {
            "old-password": "pwd",
            "new-password": "new_pwd",
            "wrong": "new_pwd"
        }
        response = client.post('/change-password', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'confirm-password'")
