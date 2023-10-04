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
        token, space_id, _ = create_space_as_admin(self.client, 'space-1')
        response = self.client.get(
            f'/spaces/{space_id}', headers={"Authorization": f"Bearer {token}"})
        data = json.loads(response.data)
        self.assertTrue("id" in data)
        self.assertTrue(isinstance(data["id"], int) and data["id"] > 0)
        self.assertEqual(data["name"], "space-1")
        self.assertEqual(response.status_code, 200)

    def test_not_exist(self):
        token, _ = register_and_login(self.client)
        response = self.client.get(
            '/spaces/999999999', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data, b"Space with ID '999999999' doesn't exist")

    def test_not_member(self):
        token, space_id = create_space_as_not_member(self.client)
        response = self.client.get(
            f'/spaces/{space_id}', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')
