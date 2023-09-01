import json
from unittest import TestCase
from test.helper import (
    register_and_login, get_app,
    logout, purge_db, create_space_as_admin,
    create_space_as_not_member
)


class TestGetSpace(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_not_logged_in(self):
        response = self.client.get('/spaces/1')
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        create_space_as_admin(self.client, 'space-1')
        response = self.client.get('/spaces/1')
        expected_data = {
            "id": 1,
            "name": "space-1"
        }
        data = json.loads(response.data)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_not_exist(self):
        register_and_login(self.client, 'usr')
        response = self.client.get('/spaces/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_not_member(self):
        create_space_as_not_member(self.client)
        response = self.client.get('/spaces/1')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')
