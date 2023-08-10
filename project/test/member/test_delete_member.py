import json
from unittest import TestCase
from test.helper import set_up, client, register, create_space_as_admin, add_member, register_and_login, logout, create_space_as_member


class TestDeleteMember(TestCase):

    def setUp(self):
        set_up()

    def test_not_logged_in(self):
        response = client.delete('/spaces/1/members/1')
        self.assertEqual(response.status_code, 401)
#

    def test_del_other_member_as_admin(self):
        register('member')
        create_space_as_admin('space-1')
        response = add_member(1, 1)

        response = client.delete('/spaces/1/members/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Member deleted')

        response = client.get('/spaces/1/members')
        expected_data = [
            {
                "is_admin": True,
                "user": {
                    "id": 2,
                    "login": "admin"
                }
            }
        ]
        data = json.loads(response.data)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_del_other_member_as_not_admin(self):
        create_space_as_member('space-1')
        response = client.delete('/spaces/1/members/2')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User not admin')

    def test_del_myself_as_member(self):
        create_space_as_member('space-1')
        response = client.delete('/spaces/1/members/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Member deleted')

    def test_del_myself_as_admin(self):
        create_space_as_admin('space-1')
        response = client.delete('/spaces/1/members/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data, b"Can\'t leave space when you\'re an admin")

    def test_space_not_exist(self):
        register('member')
        register_and_login('admin')
        response = client.delete('/spaces/999/members/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_member_not_exist(self):
        create_space_as_admin('space-1')
        response = client.delete('/spaces/1/members/999')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"User with ID '999' doesn't exist")

    def test_delete_member_from_other_space(self):
        register('member')
        create_space_as_admin('space-1')
        add_member(1, 1)
        logout()
        create_space_as_admin('space-2')
        response = client.delete('/spaces/2/members/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')
