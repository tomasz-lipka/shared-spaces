import json
from unittest import TestCase
from test.helper import set_up, client, register, create_space_as_admin, add_member, register_and_login, logout, create_space_as_member


class TestChangeAdmin(TestCase):

    def setUp(self):
        set_up()

    def test_not_logged_in(self):
        data = {
            "is-admin": True
        }
        response = client.put('/spaces/1/members/1', json=data)
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        register('member')
        create_space_as_admin('space-1')
        response = add_member(1, 1)
        data = {
            "is-admin": True
        }
        response = client.put('/spaces/1/members/1', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Admin permission changed")

        response = client.get('/spaces/1/members')
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

    def test_space_not_exist(self):
        register_and_login('admin')
        data = {
            "is-admin": True
        }
        response = client.put('/spaces/999/members/1', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_member_not_exist(self):
        create_space_as_admin('space-1')
        data = {
            "is-admin": True
        }
        response = client.put('/spaces/1/members/999', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"User with ID '999' doesn't exist")

    def test_member_from_other_space(self):
        register('member')
        create_space_as_admin('space-1')
        add_member(1, 1)
        logout()
        create_space_as_admin('space-2')

        data = {
            "is-admin": True
        }
        response = client.put('/spaces/2/members/1', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')

    def test_not_admin(self):
        create_space_as_member('space-1')
        data = {
            "is-admin": False
        }
        response = client.put('/spaces/1/members/2', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User not admin')

    def test_payload_invalid_type(self):
        register('member')
        create_space_as_admin('space-1')
        response = add_member(1, 1)
        data = {
            "is-admin": 123
        }
        response = client.put('/spaces/1/members/1', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'"is admin" must be type boolean')

    def test_wrong_json_key(self):
        register('member')
        create_space_as_admin('space-1')
        response = add_member(1, 1)
        data = {
            "wrong": True
        }
        response = client.put('/spaces/1/members/1', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'is-admin'")
