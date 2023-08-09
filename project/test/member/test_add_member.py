import json
from unittest import TestCase
from test.helper import delete_all_records_from_db, client, add_member, register, register_and_login, create_space, create_space_as_member, create_space_as_admin
# OK


class TestAddMember(TestCase):

    def setUp(self):
        delete_all_records_from_db()

    def test_not_logged_in(self):
        response = add_member(1, 1)
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        register('member')
        create_space_as_admin('space-1')
        response = add_member(1, 1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Member added")

    def test_space_not_exist(self):
        register('member')
        register_and_login('admin')
        response = add_member(999, 1)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_member_not_exist(self):
        create_space_as_admin('space-1')
        response = add_member(1, 999)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"User with ID '999' doesn't exist")

    def test_not_admin(self):
        create_space_as_member('space-1')
        response = add_member(1, 1)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User not admin')

    def test_add_member_already_added(self):
        register('member')
        create_space_as_admin('space-1')
        response = add_member(1, 1)
        response = add_member(1, 1)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"User-space pair already exists")

    def test_payload_invalid_type(self):
        register('member')
        create_space_as_admin("space-1")
        data = {
            "user-id": "wrong"
        }
        response = client.post('/spaces/1/members', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"User with ID 'wrong' doesn't exist")

    def test_wrong_json_key(self):
        register('member')
        create_space_as_admin("space-1")
        data = {
            "wrong": 1
        }
        response = client.post('/spaces/1/members', json=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload :'user-id'")
