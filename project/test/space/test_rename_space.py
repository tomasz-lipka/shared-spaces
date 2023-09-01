import json
from unittest import TestCase
from test.helper import (
    register_and_login, get_app,
    logout, purge_db, create_space_as_admin,
    create_space_as_member
)


class TestRenameSpace(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_not_logged_in(self):
        data = {
            "new-name": "space_new_name"
        }
        response = self.client.put('/spaces/1', json=data)
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        create_space_as_admin(self.client, 'space-1')
        data = {
            "new-name": "space_new_name"
        }
        response = self.client.put('/spaces/1', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Space renamed")

        response = self.client.get('/spaces/1')
        expected_data = {
            "id": 1,
            "name": "space_new_name"
        }
        data = json.loads(response.data)
        self.assertEqual(data, expected_data)

    def test_not_exist(self):
        register_and_login(self.client, 'usr')
        data = {
            "new-name": "space_new_name"
        }
        response = self.client.put('/spaces/999', json=data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_not_admin(self):
        create_space_as_member(self.client, 'space-1')
        data = {
            "new-name": "space_new_name"
        }
        response = self.client.put('/spaces/1', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User not admin')

    def test_wrong_json_key(self):
        create_space_as_admin(self.client, 'space-1')
        data = {
            "wrong": "space_new_name"
        }
        response = self.client.put('/spaces/1', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'new-name'")

    def test_null_json_value(self):
        create_space_as_admin(self.client, 'space-1')
        data = {
            "new-name": None
        }
        response = self.client.put('/spaces/1', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"New name must be provided")

    def test_empty_name(self):
        create_space_as_admin(self.client, 'space-1')
        data = {
            "new-name": "   "
        }
        response = self.client.put('/spaces/1', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Name cannot be empty")

    def test_min_char_name(self):
        create_space_as_admin(self.client, 'space-1')
        data = {
            "new-name": "a"
        }
        response = self.client.put('/spaces/1', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Name min 3 characters")

    def test_max_char_name(self):
        create_space_as_admin(self.client, 'space-1')
        data = {
            "new-name": "name name name name name"
        }
        response = self.client.put('/spaces/1', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Name max 15 characters")
