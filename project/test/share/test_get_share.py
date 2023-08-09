import json
from unittest import TestCase
import datetime
from test.helper import delete_all_records_from_db, client, create_space_as_admin, create_share, register_and_login, logout
# OK

class TestGetShare(TestCase):

    def setUp(self):
        delete_all_records_from_db()

    def test_not_logged_in(self):
        response = client.get('/shares/1')
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        create_space_as_admin('space-1')
        response = create_share(1)
        response = client.get('/shares/1')
        expected_data = {
            "id": 1,
            "space": {
                "id": 1,
                "name": "space-1"
            },
            "text": "Lorem ipsum",
            # "timestamp":,
            "user": {
                "id": 1,
                "login": "admin"
            }
        }
        data = json.loads(response.data)
        data.pop("timestamp", None)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_not_exist(self):
        register_and_login('usr')
        response = client.get('/shares/999')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'No such share')

    def test_not_owned(self):
        create_space_as_admin('space-1')
        create_share(1)
        logout()
        register_and_login('usr')
        response = client.get('/shares/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User doesn\'t own this share')
