import json
from unittest import TestCase
from test.helper import (
    get_app, logout, purge_db, create_space,
    register_and_login, WRONG_TOKEN
)


class TestCreateSpace(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_not_logged_in(self):
        response, _ = create_space(self.client, "space-1", WRONG_TOKEN)
        self.assertEqual(
            response.data, b'{"msg":"Signature verification failed"}\n')
        self.assertEqual(response.status_code, 422)

    def test_normal_run(self):
        token, _ = register_and_login(self.client, 'admin')
        response, _ = create_space(self.client, 'space-1', token)
        data = json.loads(response.data)
        self.assertTrue("id" in data)
        self.assertTrue(isinstance(data["id"], int) and data["id"] > 0)
        self.assertEqual(data["name"], "space-1")
        self.assertEqual(response.status_code, 200)

    def test_wrong_json_key(self):
        token, _ = register_and_login(self.client, 'usr')
        data = {
            "wrong": "space"
        }
        response = self.client.post(
            '/spaces', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'name'")

    def test_null_json_value(self):
        token, _ = register_and_login(self.client, 'usr')
        data = {
            "name": None
        }
        response = self.client.post(
            '/spaces', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Name must be provided")

    def test_empty_name(self):
        token, _ = register_and_login(self.client, 'usr')
        data = {
            "name": "   "
        }
        response = self.client.post(
            '/spaces', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Name cannot be empty")

    def test_min_char_name(self):
        token, _ = register_and_login(self.client, 'usr')
        data = {
            "name": "a"
        }
        response = self.client.post(
            '/spaces', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Name min 3 characters")

    def test_max_char_name(self):
        token, _ = register_and_login(self.client, 'usr')
        data = {
            "name": "name name name name name"
        }
        response = self.client.post(
            '/spaces', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Name max 15 characters")
