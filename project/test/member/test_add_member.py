from unittest import TestCase
from test.helper import get_app, add_member, WRONG_TOKEN, register, register_and_login, create_space_as_admin


class TestAddMember(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def test_not_logged_in(self):
        response = add_member(self.client, 999999999, 'member', WRONG_TOKEN)
        self.assertEqual(
            response.data, b'{"msg":"Signature verification failed"}\n')
        self.assertEqual(response.status_code, 422)

    def test_normal_run(self):
        member = register(self.client)
        token, space_id, _ = create_space_as_admin(self.client, 'space-1')
        response = add_member(self.client, space_id,
                              member.get('login'), token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Member added")

    def test_space_not_exist(self):
        member = register(self.client)
        token, _ = register_and_login(self.client)
        response = add_member(self.client, 999999999,
                              member.get('login'), token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data, b"Space with ID '999999999' doesn't exist")

    def test_member_not_exist(self):
        token, space_id, _ = create_space_as_admin(self.client, 'space-1')
        response = add_member(self.client, space_id, 'member', token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data, b"User with login 'member' doesn't exist")

    def test_not_admin(self):
        member_token, member = register_and_login(self.client)
        admin_token, space_id, _ = create_space_as_admin(
            self.client, 'space-1')
        add_member(self.client, space_id, member.get('login'), admin_token)
        response = add_member(self.client, space_id,
                              member.get('login'), member_token)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User not admin')

    def test_add_member_already_added(self):
        member = register(self.client)
        token, space_id, _ = create_space_as_admin(self.client, 'space-1')
        response = add_member(self.client, space_id,
                              member.get('login'), token)
        response = add_member(self.client, space_id,
                              member.get('login'), token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"User-space pair already exists")

    def test_payload_invalid_type(self):
        register(self.client)
        token, space_id, _ = create_space_as_admin(self.client, "space-1")
        data = {
            "login": "wrong"
        }
        response = self.client.post(
            f'/spaces/{space_id}/members', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data, b"User with login 'wrong' doesn't exist")

    def test_wrong_json_key(self):
        register(self.client)
        token, space_id, _ = create_space_as_admin(self.client, "space-1")
        data = {
            "wrong": 1
        }
        response = self.client.post(
            f'/spaces/{space_id}/members', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'login'")

    def test_null_json_value(self):
        register(self.client)
        token, space_id, _ = create_space_as_admin(self.client, "space-1")
        data = {
            "login": None
        }
        response = self.client.post(
            f'/spaces/{space_id}/members', json=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Login must be provided")
