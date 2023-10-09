import json
from unittest import TestCase
from test.helper import get_app, register, create_space_as_admin, add_member, register_and_login


class TestChangeAdmin(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def test_not_logged_in(self):
        data = {
            "is-admin": True
        }
        response = self.client.put('/spaces/1/members/1', json=data)
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        member = register(self.client)
        token, space_id, admin = create_space_as_admin(self.client, 'space-1')
        response = add_member(self.client, space_id,
                              member.get('login'), token)
        data = {
            "is-admin": True
        }
        response = self.client.put(
            f'/spaces/{space_id}/members/{member.get("id")}', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Admin permission changed")

        response = self.client.get(
            f'/spaces/{space_id}/members', headers={"Authorization": f"Bearer {token}"})
        expected_data = [
            {
                "is_admin": True,
                "user": {
                    "id": admin.get('id'),
                    "login": admin.get('login')
                }
            },
            {
                "is_admin": True,
                "user": {
                    "id": member.get('id'),
                    "login": member.get('login')
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
            f'/spaces/{space_id}/members/{member.get("id")}', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Admin permission changed")

    def test_space_not_exist(self):
        token, user = register_and_login(self.client)
        data = {
            "is-admin": True
        }
        response = self.client.put(
            f"/spaces/999999999/members/{user.get('id')}", json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data, b"Space with ID '999999999' doesn't exist")

    def test_member_not_exist(self):
        token, space_id, _ = create_space_as_admin(self.client, 'space-1')
        data = {
            "is-admin": True
        }
        response = self.client.put(
            f'/spaces/{space_id}/members/999999999', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data, b"User with ID '999999999' doesn't exist")

    def test_member_from_other_space(self):
        member = register(self.client)
        admin_1_token, space_id_1, _ = create_space_as_admin(
            self.client, 'space-1')
        add_member(self.client, space_id_1, member.get('login'), admin_1_token)
        admin_2_token, space_id_2, _ = create_space_as_admin(
            self.client, 'space-2')
        data = {
            "is-admin": True
        }
        response = self.client.put(
            f"/spaces/{space_id_2}/members/{member.get('id')}", json=data, headers={"Authorization": f"Bearer {admin_2_token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'Can\'t access this space - not a member')

    def test_not_admin(self):
        member_token, member = register_and_login(self.client)
        admin_token, space_id, admin = create_space_as_admin(
            self.client, 'space-1')
        add_member(self.client, space_id, member.get('login'), admin_token)
        data = {
            "is-admin": False
        }
        response = self.client.put(
            f"/spaces/{space_id}/members/{admin.get('id')}", json=data, headers={"Authorization": f"Bearer {member_token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User not admin')

    def test_payload_invalid_type(self):
        member = register(self.client)
        token, space_id, _ = create_space_as_admin(self.client, 'space-1')
        response = add_member(self.client, space_id,
                              member.get('login'), token)
        data = {
            "is-admin": 123
        }
        response = self.client.put(
            f"/spaces/{space_id}/members/{member.get('id')}", json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'"is admin" must be type boolean')

    def test_wrong_json_key(self):
        member = register(self.client)
        token, space_id, _ = create_space_as_admin(self.client, 'space-1')
        response = add_member(self.client, space_id,
                              member.get('login'), token)
        data = {
            "wrong": True
        }
        response = self.client.put(
            f"/spaces/{space_id}/members/{member.get('id')}", json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'is-admin'")

    def test_null_json_value(self):
        member = register(self.client)
        token, space_id, _ = create_space_as_admin(self.client, 'space-1')
        response = add_member(self.client, space_id,
                              member.get('login'), token)
        data = {
            "is-admin": None
        }
        response = self.client.put(
            f"/spaces/{space_id}/members/{member.get('id')}", json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Is admin must be provided")

    def test_last_admin(self):
        token, space_id, user = create_space_as_admin(self.client, 'space-1')
        data = {
            "is-admin": False
        }
        response = self.client.put(
            f"/spaces/{space_id}/members/{user.get('id')}", json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space must have at least one admin")

    def test_only_admin(self):
        member = register(self.client)
        token, space_id, admin = create_space_as_admin(self.client, 'space-1')
        data = {
            "is-admin": False
        }
        add_member(self.client, space_id, member.get('login'), token)
        response = self.client.put(
            f"/spaces/{space_id}/members/{admin.get('id')}", json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space must have at least one admin")
