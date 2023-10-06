import json
from unittest import TestCase
from test.helper import get_app, register, create_space_as_admin, add_member, register_and_login, create_space


class TestGetMembers(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def test_not_logged_in(self):
        response = self.client.get('/spaces/1/members')
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        member_1 = register(self.client)
        member_2 = register(self.client)
        token, space_id_1, admin = create_space_as_admin(
            self.client, 'space-1')
        response, space_id_2 = create_space(self.client, 'space-2', token)
        add_member(self.client, space_id_1, member_1.get('login'), token)
        add_member(self.client, space_id_2,  member_2.get('login'), token)

        response = self.client.get(
            f'/spaces/{space_id_1}/members', headers={"Authorization": f"Bearer {token}"})
        expected_data = [
            {
                "is_admin": True,
                "user": {
                    "id": admin.get('id'),
                    "login": admin.get('login')
                }
            },
            {
                "is_admin": False,
                "user": {
                    "id": member_1.get('id'),
                    "login": member_1.get('login')
                }
            }
        ]
        data = json.loads(response.data)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_space_not_exist(self):
        token, _ = register_and_login(self.client)
        response = self.client.get(
            '/spaces/999999999/members', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data, b"Space with ID '999999999' doesn't exist")

    def test_not_member(self):
        _, space_id, _ = create_space_as_admin(self.client, 'space-1')
        not_member_token, _ = register_and_login(self.client)
        response = self.client.get(
            f'/spaces/{space_id}/members', headers={"Authorization": f"Bearer {not_member_token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')
