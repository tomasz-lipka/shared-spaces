import json
from unittest import TestCase
from test.helper import (
    get_app, logout, purge_db, create_space_as_admin,
    create_share, register_and_login
)


class TestEditShare(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_not_logged_in(self):
        data = {
            "text": "Edit lorem ipsum"
        }
        response = self.client.put('/shares/1', json=data)
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        create_space_as_admin(self.client, 'space-1')
        create_share(self.client, 1)
        data = {
            "text": "Edit lorem ipsum"
        }
        response = self.client.put('/shares/1', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Share edited")

        response = self.client.get('/shares/1')
        expected_data = {
            "id": 1,
            "space": {
                "id": 1,
                "name": "space-1"
            },
            # "timestamp":,
            "user": {
                "id": 1,
                "login": "admin"
            },
            "text": "Edit lorem ipsum",
            "media_url": None
        }
        data = json.loads(response.data)
        data.pop("timestamp", None)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_not_owned(self):
        create_space_as_admin(self.client, 'space-1')
        create_share(self.client, 1)
        logout(self.client)
        register_and_login(self.client, 'usr')

        data = {
            "text": "Edit lorem ipsum"
        }
        response = self.client.put('/shares/1', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User doesn\'t own this share')

    def test_not_exist(self):
        register_and_login(self.client, 'usr')
        data = {
            "text": "Edit lorem ipsum"
        }
        response = self.client.put('/shares/1', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'No such share')

    def test_wrong_json_key(self):
        create_space_as_admin(self.client, 'space-1')
        create_share(self.client, 1)
        data = {
            "wrong": "Edit lorem ipsum"
        }
        response = self.client.put('/shares/1', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'text'")
