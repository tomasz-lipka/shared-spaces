import json
from unittest import TestCase
from test.helper import register_and_login, delete_all_records_from_db, client, create_space, create_space_as_not_member
# OK


class TestGetSpaces(TestCase):

    def setUp(self):
        delete_all_records_from_db()

    def test_not_logged_in(self):
        response = client.get('/spaces')
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        register_and_login('usr')
        create_space("space-1")
        create_space("space-2")
        response = client.get('/spaces')
        expected_data = [
            {
                "is_admin": True,
                "space": {
                    "id": 1,
                    "name": "space-1"
                }
            },
            {
                "is_admin": True,
                "space": {
                    "id": 2,
                    "name": "space-2"
                }
            }
        ]
        data = json.loads(response.data)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_not_member(self):
        create_space_as_not_member()
        create_space('space-2')
        response = client.get('/spaces')
        expected_data = [
            {
                "is_admin": True,
                "space": {
                    "id": 2,
                    "name": "space-2"
                }
            }
        ]
        data = json.loads(response.data)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)
