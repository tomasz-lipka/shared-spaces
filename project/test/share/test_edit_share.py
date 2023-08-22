import json
from unittest import TestCase
from test.helper import set_up, client, create_space_as_admin, create_share, logout, register_and_login


class TestEditShare(TestCase):

    def setUp(self):
        set_up()

    def test_not_logged_in(self):
        data = {
            "text": "Edit lorem ipsum"
        }
        response = client.put('/shares/1', json=data)
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        create_space_as_admin('space-1')
        create_share(1)
        data = {
            "text": "Edit lorem ipsum"
        }
        response = client.put('/shares/1', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Share edited")

        response = client.get('/shares/1')
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
        create_space_as_admin('space-1')
        create_share(1)
        logout()
        register_and_login('usr')

        data = {
            "text": "Edit lorem ipsum"
        }
        response = client.put('/shares/1', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User doesn\'t own this share')

    def test_not_exist(self):
        register_and_login('usr')
        data = {
            "text": "Edit lorem ipsum"
        }
        response = client.put('/shares/1', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'No such share')

    def test_wrong_json_key(self):
        create_space_as_admin('space-1')
        create_share(1)
        data = {
            "wrong": "Edit lorem ipsum"
        }
        response = client.put('/shares/1', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload :'text'")
