from unittest import TestCase
from test.helper import (
    get_app, create_space_as_admin,
    create_share, register_and_login,
    create_share_with_image, find_bucket, login
)


class TestDeleteShare(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def test_not_logged_in(self):
        response = self.client.delete('/shares/1')
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        token, space_id, _ = create_space_as_admin(self.client, 'space-1')
        _, share_id = create_share(self.client, space_id, token)
        response = self.client.delete(
            f'/shares/{share_id}', headers={"Authorization": f"Bearer {token}"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Share deleted")

        response = self.client.get(
            f'/shares/{share_id}', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b'No such share')

    def test_not_owned(self):
        token, space_id, _ = create_space_as_admin(self.client, 'space-1')
        _, share_id = create_share(self.client, space_id, token)
        token, _ = register_and_login(self.client)

        response = self.client.delete(
            f'/shares/{share_id}', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User doesn\'t own this share')

    def test_not_exist(self):
        token, _ = register_and_login(self.client)
        response = self.client.delete(
            '/shares/999999999', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b'No such share')

    def test_not_owned_with_image(self):
        token, space_id, admin = create_space_as_admin(self.client, 'space-1')
        _, share_id = create_share_with_image(
            self.client, space_id, 'test-image-1.jpg', token)
        token, _ = register_and_login(self.client)

        response = self.client.delete(
            f'/shares/{share_id}', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User doesn\'t own this share')
        self.assertTrue(find_bucket(f'test-space-id-{space_id}'))

        token = login(self.client, admin.get('login'))
        self.client.delete(
            f'/spaces/{space_id}', headers={"Authorization": f"Bearer {token}"})
