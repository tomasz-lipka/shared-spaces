import time
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
        token, space_id, _ = create_space_as_admin(self.client, 'space-1')
        response = self.client.delete(
            f'/spaces/{space_id}', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Space deleted")

        response = self.client.get(
            f'/spaces/{space_id}', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data, f"Space with ID '{space_id}' doesn't exist".encode())

    def test_not_exist(self):
        token, _ = register_and_login(self.client, 'usr')
        response = self.client.delete(
            '/spaces/999999999', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data, b"Space with ID '999999999' doesn't exist")

    def test_not_admin(self):
        token, space_id = create_space_as_member(self.client, 'space-1')
        response = self.client.delete(
            f'/spaces/{space_id}', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User not admin')

    def test_not_empty(self):
        register(self.client, 'member')
        token, space_id, _ = create_space_as_admin(self.client, 'space-1')
        add_member(self.client, space_id, 'member', token)
        response = self.client.delete(
            f'/spaces/{space_id}', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'Space not empty')

    def test_delete_s3_bucket(self):
        token, space_id, _ = create_space_as_admin(self.client, 'space-1')
        create_share_with_image(
            self.client, space_id, 'test-image-1.jpg', token)
        self.client.delete(
            f'/spaces/{space_id}', headers={"Authorization": f"Bearer {token}"})
        count = 0
        while find_bucket(f'test-space-id-{space_id}') and count < 3:
            time.sleep(1)
            count = +1
        self.assertFalse(find_bucket(f'test-space-id-{space_id}'))
