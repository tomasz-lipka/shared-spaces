import json
from unittest import TestCase
from test.helper import register_and_login,  delete_all_records_from_db, client, logout
from test.test_create_space import create_space


class TestGetSpace(TestCase):

    def setUp(self):
        delete_all_records_from_db()

    def test_not_logged_in(self):
        response = client.get('/spaces/1')
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        register_and_login('usr')
        create_space("space-1")
        response = client.get('/spaces/1')
        expected_data = {
            "id": 1,
            "name": "space-1"
        }
        data = json.loads(response.data)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_not_exist(self):
        register_and_login('usr')
        response = client.get('/spaces/999')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_not_member(self):
        register_and_login('other-usr')
        create_space('other-space')
        logout()
        register_and_login('usr')
        response = client.get('/spaces/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')
