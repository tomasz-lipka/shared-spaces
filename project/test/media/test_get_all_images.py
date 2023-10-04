from unittest import TestCase
import json
from test.helper import (
    get_app, logout, purge_db, create_share_with_image, register_and_login,
    create_space_as_admin, are_images_same, create_space_as_not_member, find_bucket
)


class TestGetAllImages(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_not_logged_in(self):
        response = self.client.get('/spaces/1/images')
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        token, space_id, _ = create_space_as_admin(self.client, 'space-1')
        create_share_with_image(
            self.client, space_id, 'test-image-1.jpg', token)
        create_share_with_image(
            self.client, space_id, 'test-image-2.jpg', token)
        response = self.client.get(
            f'/spaces/{space_id}/images', headers={"Authorization": f"Bearer {token}"})
        data = json.loads(response.data)

        self.assertTrue(are_images_same(
            data[0], 'test-image-1.jpg'))
        self.assertTrue(are_images_same(
            data[1], 'test-image-2.jpg'))

        self.client.delete(
            f'/spaces/{space_id}', headers={"Authorization": f"Bearer {token}"})

    def test_space_not_exist(self):
        token, _ = register_and_login(self.client)
        response = self.client.get(
            '/spaces/999999999/images', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data, b"Space with ID '999999999' doesn't exist")

    def test_not_member(self):
        token, space_id = create_space_as_not_member(self.client)
        response = self.client.get(
            f'/spaces/{space_id}/images', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')

    def test_no_images(self):
        token, space_id, _ = create_space_as_admin(self.client, 'space-1')
        response = self.client.get(
            f'/spaces/{space_id}/images', headers={"Authorization": f"Bearer {token}"})
        expected_data = []
        data = json.loads(response.data)
        self.assertEqual(data, expected_data)

    def test_is_temp_bucket_created(self):
        self.assertTrue(find_bucket('shared-spaces-temp'))
