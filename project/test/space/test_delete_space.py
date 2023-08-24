from unittest import TestCase
from test.helper import (
    register_and_login, get_app, logout, purge_db, create_space_as_admin,
    create_space_as_member, add_member,
    register, create_share_with_image, find_bucket
)


class TestDeleteSpace(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_not_logged_in(self):
        response = self.client.delete('/spaces/1')
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        create_space_as_admin(self.client, 'space-1')
        response = self.client.delete('/spaces/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Space deleted")

        response = self.client.get('/spaces/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '1' doesn't exist")

    def test_not_exist(self):
        register_and_login(self.client, 'usr')
        response = self.client.delete('/spaces/999')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_not_admin(self):
        create_space_as_member(self.client, 'space-1')
        response = self.client.delete('/spaces/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User not admin')

    def test_not_empty(self):
        register(self.client, 'member')
        create_space_as_admin(self.client, 'space-1')
        add_member(self.client, 1, 1)
        response = self.client.delete('/spaces/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'Space not empty')

    def test_delete_s3_bucket(self):
        create_space_as_admin(self.client, 'space-1')
        create_share_with_image(self.client, 1)
        self.client.delete('/spaces/1')

        self.assertFalse(find_bucket('space-id-1'))
