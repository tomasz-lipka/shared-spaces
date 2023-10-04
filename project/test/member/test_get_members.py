import json
from unittest import TestCase
from test.helper import (
    get_app, logout, purge_db, register, create_space_as_admin,
    add_member, register_and_login, create_space
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
        member_1 = register(self.client, 'member-1')
        register(self.client, 'member-2')
        token, space_id_1, admin = create_space_as_admin(
            self.client, 'space-1')
        response, space_id_2 = create_space(self.client, 'space-2', token)
        add_member(self.client, space_id_1, 'member-1', token)
        add_member(self.client, space_id_2, 'member-2', token)

        response = self.client.get(
            f'/spaces/{space_id_1}/members', headers={"Authorization": f"Bearer {token}"})
        expected_data = [
            {
                "is_admin": True,
                "user": {
                    "id": admin.get('id'),
                    "login": "admin"
                }
            },
            {
                "is_admin": False,
                "user": {
                    "id": member_1.get('id'),
                    "login": "member-1"
                }
            }
        ]
        data = json.loads(response.data)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_space_not_exist(self):
        token, _ = register_and_login(self.client, 'admin')
        response = self.client.get(
            '/spaces/999999999/members', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data, b"Space with ID '999999999' doesn't exist")

    def test_not_member(self):
        token, space_id, _ = create_space_as_admin(self.client, 'space-1')
        logout(self.client)
        token, _ = register_and_login(self.client, 'member')
        response = self.client.get(
            f'/spaces/{space_id}/members', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')
