import json
from unittest import TestCase
from test.helper import (
    get_app, logout, purge_db, register, create_space_as_admin,
    add_member, register_and_login,
    create_space_as_not_member, create_space
)


class TestGetMembers(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_not_logged_in(self):
        response = self.client.get('/spaces/1/members')
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        register(self.client, 'member-1')
        register(self.client, 'member-2')
        token = create_space_as_admin(self.client, 'space-1')
        create_space(self.client, 'space-2', token)
        add_member(self.client, 1, 1, token)
        add_member(self.client, 2, 2, token)

        response = self.client.get(
            '/spaces/1/members', headers={"Authorization": f"Bearer {token}"})
        expected_data = [
            {
                "is_admin": True,
                "user": {
                    "id": 3,
                    "login": "admin"
                }
            },
            {
                "is_admin": False,
                "user": {
                    "id": 1,
                    "login": "member-1"
                }
            }
        ]
        data = json.loads(response.data)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_space_not_exist(self):
        token = register_and_login(self.client, 'admin')
        response = self.client.get(
            '/spaces/999/members', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_not_member(self):
        token = create_space_as_not_member(self.client)
        response = self.client.get(
            '/spaces/1/members', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')
