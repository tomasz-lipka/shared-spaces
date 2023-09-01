from unittest import TestCase
from test.helper import (
    get_app, logout, purge_db, add_member,
    register, register_and_login,
    create_space_as_member, create_space_as_admin
)


class TestAddMember(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_not_logged_in(self):
        response = add_member(self.client, 1, 1)
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        register(self.client, 'member')
        create_space_as_admin(self.client, 'space-1')
        response = add_member(self.client, 1, 1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Member added")

    def test_space_not_exist(self):
        register(self.client, 'member')
        register_and_login(self.client, 'admin')
        response = add_member(self.client, 999, 1)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_member_not_exist(self):
        create_space_as_admin(self.client, 'space-1')
        response = add_member(self.client, 1, 999)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b"User with ID '999' doesn't exist")

    def test_not_admin(self):
        create_space_as_member(self.client, 'space-1')
        response = add_member(self.client, 1, 1)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User not admin')

    def test_add_member_already_added(self):
        register(self.client, 'member')
        create_space_as_admin(self.client, 'space-1')
        response = add_member(self.client, 1, 1)
        response = add_member(self.client, 1, 1)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"User-space pair already exists")

    def test_payload_invalid_type(self):
        register(self.client, 'member')
        create_space_as_admin(self.client, "space-1")
        data = {
            "user-id": "wrong"
        }
        response = self.client.post('/spaces/1/members', json=data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b"User with ID 'wrong' doesn't exist")

    def test_wrong_json_key(self):
        register(self.client, 'member')
        create_space_as_admin(self.client, "space-1")
        data = {
            "wrong": 1
        }
        response = self.client.post('/spaces/1/members', json=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'user-id'")

    def test_null_json_value(self):
        register(self.client, 'member')
        create_space_as_admin(self.client, "space-1")
        data = {
            "user-id": None
        }
        response = self.client.post('/spaces/1/members', json=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"User id must be provided")
