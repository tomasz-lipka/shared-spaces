from unittest import TestCase
from test.helper import get_app, logout, purge_db, register_and_login, WRONG_TOKEN


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
        response = self.client.put(
            '/change-password', json=data, headers={"Authorization": f"Bearer {WRONG_TOKEN}"})
        self.assertEqual(
            response.data, b'{"msg":"Signature verification failed"}\n')
        self.assertEqual(response.status_code, 422)

    def test_normal_run(self):
        token, _ = register_and_login(self.client, 'usr')
        data = {
            "old-password": "pwd",
            "new-password": "new_pwd",
            "confirm-password": "new_pwd"
        }
        response = self.client.put(
            '/change-password', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Password changed")

        logout(self.client)
        data = {
            "login": 'usr',
            "password": "new_pwd"
        }
        response = self.client.post(
            '/login', json=data)
        self.assertEqual(response.status_code, 200)

    def test_wrong_old_pwd(self):
        token, _ = register_and_login(self.client, 'usr')
        data = {
            "old-password": "wrong",
            "new-password": "new_pwd",
            "confirm-password": "new_pwd"
        }
        response = self.client.put(
            '/change-password', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, b"Wrong password")

    def test_wrong_confirmation(self):
        token, _ = register_and_login(self.client, 'usr')
        data = {
            "old-password": "pwd",
            "new-password": "new_pwd",
            "confirm-password": "wrong_new_pwd"
        }
        response = self.client.put(
            '/change-password', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"New passwords don\'t match")

    def test_wrong_json_key_old_pwd(self):
        token, _ = register_and_login(self.client, 'usr')
        data = {
            "wrong": "pwd",
            "new-password": "new_pwd",
            "confirm-password": "new_pwd"
        }
        response = self.client.put(
            '/change-password', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'old-password'")

    def test_wrong_json_key_new_pwd(self):
        token, _ = register_and_login(self.client, 'usr')
        data = {
            "old-password": "pwd",
            "wrong": "new_pwd",
            "confirm-password": "new_pwd"
        }
        response = self.client.put(
            '/change-password', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'new-password'")

    def test_wrong_json_key_confirm_pwd(self):
        token = register_and_login(self.client, 'usr')
        data = {
            "old-password": "pwd",
            "new-password": "new_pwd",
            "wrong": "new_pwd"
        }
        response = self.client.put(
            '/change-password', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'confirm-password'")

    def test_null_json_value_old_pwd(self):
        token, _ = register_and_login(self.client, 'usr')
        data = {
            "old-password": None,
            "new-password": "new_pwd",
            "confirm-password": "new_pwd"
        }
        response = self.client.put(
            '/change-password', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Old password must be provided")

    def test_null_json_value_new_pwd(self):
        token, _ = register_and_login(self.client, 'usr')
        data = {
            "old-password": "pwd",
            "new-password": None,
            "confirm-password": "new_pwd"
        }
        response = self.client.put(
            '/change-password', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"New password must be provided")

    def test_null_json_value_confirm_pwd(self):
        token, _ = register_and_login(self.client, 'usr')
        data = {
            "old-password": "pwd",
            "new-password": "new_pwd",
            "confirm-password": None
        }
        response = self.client.put(
            '/change-password', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Confirm password must be provided")

    def test_empty_new_pwd(self):
        token, _ = register_and_login(self.client, 'usr')
        data = {
            "old-password": "pwd",
            "new-password": "   ",
            "confirm-password": "new_pwd"
        }
        response = self.client.put(
            '/change-password', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"New password cannot be empty")

    def test_min_char_new_pwd(self):
        token, _ = register_and_login(self.client, 'usr')
        data = {
            "old-password": "pwd",
            "new-password": "a",
            "confirm-password": "new_pwd"
        }
        response = self.client.put(
            '/change-password', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"New password min 3 characters")
