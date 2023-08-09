import json
from unittest import TestCase
import datetime
from test.helper import delete_all_records_from_db, client, create_share, logout, register_and_login, create_space, register, add_member, login, create_space_as_not_member
# OK

class TestGetShares(TestCase):

    def setUp(self):
        delete_all_records_from_db()

    def test_not_logged_in(self):
        response = client.get('/spaces/1/shares')
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        register_and_login('admin-1')
        create_space('space-1')
        create_share(1)
        logout()

        register('member-1')

        register_and_login('admin-2')
        create_space('space-2')
        create_share(2)
        add_member(2, 2)
        logout()

        login('member-1')
        create_share(2)

        response = client.get('/spaces/2/shares')
        expected_data = [
            {
                "id": 2,
                "text": "Lorem ipsum",
                # "timestamp":,
                "user": {
                    "id": 3,
                    "login": "admin-2"
                }
            },
            {
                "id": 3,
                "text": "Lorem ipsum",
                # "timestamp":,
                "user": {
                    "id": 2,
                    "login": "member-1"
                }
            }
        ]
        data = json.loads(response.data)
        for item in data:
            item.pop("timestamp", None)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_space_not_exist(self):
        register_and_login('usr')
        response = client.get('/spaces/999/shares')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_not_member(self):
        create_space_as_not_member()
        response = client.get('/spaces/1/shares')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')
