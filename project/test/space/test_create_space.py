from unittest import TestCase
from test.helper import (
    get_app, logout, purge_db, create_space,
    create_space_as_admin, register_and_login
)


class TestCreateSpace(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_not_logged_in(self):
        response = create_space(self.client, "space-1")
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        response = create_space_as_admin(self.client, 'space-1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Space created")

    def test_wrong_json_key(self):
        register_and_login(self.client, 'usr')
        data = {
            "wrong": "space"
        }
        response = self.client.post('/spaces', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'name'")

    def test_null_json_value(self):
        register_and_login(self.client, 'usr')
        data = {
            "name": None
        }
        response = self.client.post('/spaces', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Name must be provided")

    def test_empty_name(self):
        register_and_login(self.client, 'usr')
        data = {
            "name": "   "
        }
        response = self.client.post('/spaces', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Name cannot be empty")

    def test_min_char_name(self):
        register_and_login(self.client, 'usr')
        data = {
            "name": "a"
        }
        response = self.client.post('/spaces', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Name min 3 characters")

    def test_max_char_name(self):
        register_and_login(self.client, 'usr')
        data = {
            "name": "name name name name name"
        }
        response = self.client.post('/spaces', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Name max 10 characters")
