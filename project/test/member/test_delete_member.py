import json
from unittest import TestCase
from test.helper import (
    get_app, logout, purge_db, register,
    create_space_as_admin, add_member, login,
    register_and_login
)


class TestDeleteMember(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_not_logged_in(self):
        response = self.client.delete('/spaces/1/members/1')
        self.assertEqual(response.status_code, 401)

    def test_del_other_member_as_admin(self):
        member = register(self.client)
        token, space_id, admin = create_space_as_admin(self.client, 'space-1')
        response = add_member(self.client, space_id,
                              member.get('login'), token)

        response = self.client.delete(
            f"/spaces/{space_id}/members/{member.get('id')}", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Member deleted')

        response = self.client.get(
            f'/spaces/{space_id}/members', headers={"Authorization": f"Bearer {token}"})
        expected_data = [
            {
                "is_admin": True,
                "user": {
                    "id": admin.get('id'),
                    "login": admin.get('login')
                }
            }
        ]
        data = json.loads(response.data)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_del_other_member_as_not_admin(self):
        member = register(self.client)
        token, space_id, admin = create_space_as_admin(self.client, 'space-1')
        add_member(self.client, space_id, member.get('login'), token)
        logout(self.client)
        token = login(self.client, member.get('login'))
        response = self.client.delete(
            f"/spaces/{space_id}/members/{admin.get('id')}", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User not admin')

    def test_del_myself_as_member(self):
        member = register(self.client)
        token, space_id, _ = create_space_as_admin(self.client, 'space-1')
        add_member(self.client, space_id, member.get('login'), token)
        logout(self.client)
        token = login(self.client, member.get('login'))
        response = self.client.delete(
            f'/spaces/{space_id}/members/{member.get("id")}', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Member deleted')

    def test_del_myself_as_admin(self):
        token, space_id, admin = create_space_as_admin(self.client, 'space-1')
        response = self.client.delete(
            f'/spaces/{space_id}/members/{admin.get("id")}', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data, b"Can\'t leave space when you\'re an admin")

    def test_space_not_exist(self):
        member = register(self.client)
        token, _ = register_and_login(self.client)
        response = self.client.delete(
            f'/spaces/999999999/members/{member.get("id")}', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data, b"Space with ID '999999999' doesn't exist")

    def test_member_not_exist(self):
        token, space_id, _ = create_space_as_admin(self.client, 'space-1')
        response = self.client.delete(
            f'/spaces/{space_id}/members/999999999', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data, b"User with ID '999999999' doesn't exist")

    def test_delete_member_from_other_space(self):
        member = register(self.client)
        token, space_id_1, _ = create_space_as_admin(
            self.client, 'space-1')
        add_member(self.client, space_id_1, member.get('login'), token)
        logout(self.client)
        token, space_id_2, _ = create_space_as_admin(
            self.client, 'space-2')
        response = self.client.delete(
            f'/spaces/{space_id_2}/members/{member.get("id")}', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')
