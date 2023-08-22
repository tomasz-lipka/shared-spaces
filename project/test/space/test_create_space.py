import json
from unittest import TestCase
from test.helper import set_up, client, create_space, create_space_as_admin


class TestCreateSpace(TestCase):

    def setUp(self):
        set_up()

    def test_not_logged_in(self):
        response = create_space("space-1")
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        response = create_space_as_admin('space-1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Space created")

    def test_wrong_json_key(self):
        data = {
            "wrong": "space"
        }
        response = client.post('/spaces', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'name'")
