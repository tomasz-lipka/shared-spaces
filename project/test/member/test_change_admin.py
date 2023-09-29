import json
from unittest import TestCase
from test.helper import (
    get_app, logout, purge_db, register,
    create_space_as_admin, add_member,
    register_and_login, create_space_as_member
)


class TestChangeAdmin(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_not_logged_in(self):
        data = {
            "is-admin": True
        }
        response = self.client.put('/spaces/1/members/1', json=data)
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        register(self.client, 'member')
        token = create_space_as_admin(self.client, 'space-1')
        response = add_member(self.client, 1, 'member', token)
        data = {
            "is-admin": True
        }
        response = self.client.put(
            '/spaces/1/members/1', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Admin permission changed")

        response = self.client.get(
            '/spaces/1/members', headers={"Authorization": f"Bearer {token}"})
        expected_data = [
            {
                "is_admin": True,
                "user": {
                    "id": 2,
                    "login": "admin"
                }
            },
            {
                "is_admin": True,
                "user": {
                    "id": 1,
                    "login": "member"
                }
            }
        ]
        data = json.loads(response.data)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

        data = {
            "is-admin": False
        }
        response = self.client.put(
            '/spaces/1/members/1', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Admin permission changed")

    def test_space_not_exist(self):
        token = register_and_login(self.client, 'admin')
        data = {
            "is-admin": True
        }
        response = self.client.put(
            '/spaces/999/members/1', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_member_not_exist(self):
        token = create_space_as_admin(self.client, 'space-1')
        data = {
            "is-admin": True
        }
        response = self.client.put(
            '/spaces/1/members/999', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b"User with ID '999' doesn't exist")

    def test_member_from_other_space(self):
        register(self.client, 'member')
        token = create_space_as_admin(self.client, 'space-1')
        add_member(self.client, 1, 'member', token)
        logout(self.client)
        token = create_space_as_admin(self.client, 'space-2')

        data = {
            "is-admin": True
        }
        response = self.client.put(
            '/spaces/2/members/1', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')

    def test_not_admin(self):
        token = create_space_as_member(self.client, 'space-1')
        data = {
            "is-admin": False
        }
        response = self.client.put(
            '/spaces/1/members/2', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User not admin')

    def test_payload_invalid_type(self):
        register(self.client, 'member')
        token = create_space_as_admin(self.client, 'space-1')
        response = add_member(self.client, 1, 'member', token)
        data = {
            "is-admin": 123
        }
        response = self.client.put(
            '/spaces/1/members/1', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'"is admin" must be type boolean')

    def test_wrong_json_key(self):
        register(self.client, 'member')
        token = create_space_as_admin(self.client, 'space-1')
        response = add_member(self.client, 1, 'member', token)
        data = {
            "wrong": True
        }
        response = self.client.put(
            '/spaces/1/members/1', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'is-admin'")

    def test_null_json_value(self):
        register(self.client, 'member')
        token = create_space_as_admin(self.client, 'space-1')
        response = add_member(self.client, 1, 'member', token)
        data = {
            "is-admin": None
        }
        response = self.client.put(
            '/spaces/1/members/1', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Is admin must be provided")

    def test_last_admin(self):
        token = create_space_as_admin(self.client, 'space-1')
        data = {
            "is-admin": False
        }
        response = self.client.put(
            '/spaces/1/members/1', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space must have at least one admin")

    def test_only_admin(self):
        register(self.client, 'member')
        token = create_space_as_admin(self.client, 'space-1')
        data = {
            "is-admin": False
        }
        add_member(self.client, 1, 'member', token)
        response = self.client.put(
            '/spaces/1/members/2', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space must have at least one admin")
