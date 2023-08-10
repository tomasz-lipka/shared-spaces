import json
from unittest import TestCase
from test.helper import set_up, client, register, create_space_as_admin, add_member, register_and_login, create_space_as_not_member, create_space
 

class TestGetMembers(TestCase):

    def setUp(self):
        set_up()

    def test_not_logged_in(self):
        response = client.get('/spaces/1/members')
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        register('member-1')
        register('member-2')
        create_space_as_admin('space-1')
        create_space('space-2')
        add_member(1, 1)
        add_member(2, 2)

        response = client.get('/spaces/1/members')
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
        register_and_login('admin')
        response = client.get('/spaces/999/members')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_not_member(self):
        create_space_as_not_member()
        response = client.get('/spaces/1/members')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')
