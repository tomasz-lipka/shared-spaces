from unittest import TestCase
from test.helper import (
    get_app, logout, purge_db, create_space,
    create_space_as_admin, register_and_login
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
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NDE2NDIwMSwianRpIjoiNjc0NmNhZGEtNzFjYS00ZGZhLWFkYTUtOTFhYTRlODg2YzZmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRvbSIsIm5iZiI6MTY5NDE2NDIwMSwiZXhwIjoxNjk0MTY1MTAxfQ.GPN8b1ahikw28Iy8cv3zr3gv_MqHfxZktU5zWEiFGT8"
        response = create_space(self.client, "space-1", token)
        self.assertEqual(
            response.data, b'{"msg":"Signature verification failed"}\n')
        self.assertEqual(response.status_code, 422)

    def test_normal_run(self):
        token = register_and_login(self.client, 'admin')
        response = create_space(self.client, 'space-1', token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Space created")

    def test_wrong_json_key(self):
        token = register_and_login(self.client, 'usr')
        data = {
            "wrong": "space"
        }
        response = self.client.post(
            '/spaces', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'name'")

    def test_null_json_value(self):
        token = register_and_login(self.client, 'usr')
        data = {
            "name": None
        }
        response = self.client.post(
            '/spaces', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Name must be provided")

    def test_empty_name(self):
        token = register_and_login(self.client, 'usr')
        data = {
            "name": "   "
        }
        response = self.client.post(
            '/spaces', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Name cannot be empty")

    def test_min_char_name(self):
        token = register_and_login(self.client, 'usr')
        data = {
            "name": "a"
        }
        response = self.client.post(
            '/spaces', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Name min 3 characters")

    def test_max_char_name(self):
        token = register_and_login(self.client, 'usr')
        data = {
            "name": "name name name name name"
        }
        response = self.client.post(
            '/spaces', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Name max 15 characters")
