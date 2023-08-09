import json
from unittest import TestCase
from test.helper import delete_all_records_from_db, client, create_space_as_admin, register_and_login, create_share, create_space_as_not_member
# OK

class TestCreateShare(TestCase):

    def setUp(self):
        delete_all_records_from_db()

    def test_not_logged_in(self):
        response = create_share(1)
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        create_space_as_admin('space-1')
        response = create_share(1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Share created")

    def test_space_not_exist(self):
        register_and_login('admin')
        response = create_share(999)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_not_member(self):
        create_space_as_not_member()
        response = create_share(1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')

    def test_wrong_json_key(self):
        create_space_as_admin('space-1')
        data = {
            "wrong": "Lorem ipsum"
        }
        response = client.post('/spaces/1/shares', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload :'text'")
