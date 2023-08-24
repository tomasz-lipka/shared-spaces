from unittest import TestCase
from test.helper import get_app, logout, purge_db, create_space, create_space_as_admin


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
        data = {
            "wrong": "space"
        }
        response = self.client.post('/spaces', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'name'")
