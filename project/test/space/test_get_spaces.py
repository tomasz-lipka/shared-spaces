import json
from unittest import TestCase
from test.helper import register_and_login, get_app, logout, purge_db, create_space, create_space_as_not_member


class TestGetSpaces(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_not_logged_in(self):
        response = self.client.get('/spaces')
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        register_and_login(self.client, 'usr')
        create_space(self.client, "space-1")
        create_space(self.client, "space-2")
        response = self.client.get('/spaces')
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
        create_space_as_not_member(self.client)
        create_space(self.client, 'space-2')
        response = self.client.get('/spaces')
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
