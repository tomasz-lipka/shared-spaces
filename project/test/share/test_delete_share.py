from unittest import TestCase
from test.helper import (
    get_app, logout, purge_db, create_space_as_admin,
    create_share, register_and_login,
    create_share_with_image, find_bucket, login
)


class TestDeleteShare(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_not_logged_in(self):
        response = self.client.delete('/shares/1')
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        token = create_space_as_admin(self.client, 'space-1')
        create_share(self.client, 1, token)
        response = self.client.delete(
            '/shares/1', headers={"Authorization": f"Bearer {token}"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Share deleted")

        response = self.client.get(
            '/shares/1', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b'No such share')

    def test_not_owned(self):
        token = create_space_as_admin(self.client, 'space-1')
        create_share(self.client, 1, token)
        logout(self.client)
        token = register_and_login(self.client, 'usr')

        response = self.client.delete(
            '/shares/1', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User doesn\'t own this share')

    def test_not_exist(self):
        token = register_and_login(self.client, 'usr')
        response = self.client.delete(
            '/shares/1', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b'No such share')

    def test_not_owned_with_image(self):
        token = create_space_as_admin(self.client, 'space-1')
        create_share_with_image(
            self.client, 1, '/workspaces/shared-spaces/project/test/resources/test-image-1.jpg', token)
        logout(self.client)
        token = register_and_login(self.client, 'usr')

        response = self.client.delete(
            '/shares/1', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User doesn\'t own this share')
        self.assertTrue(find_bucket('test-space-id-1'))

        logout(self.client)
        token = login(self.client, 'admin')
        self.client.delete(
            '/spaces/1', headers={"Authorization": f"Bearer {token}"})
