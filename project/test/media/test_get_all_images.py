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
        create_space_as_admin(self.client, 'space-1')
        create_share_with_image(
            self.client, 1, '/workspaces/shared-spaces/project/test/resources/test-image-1.jpg')
        create_share_with_image(
            self.client, 1, '/workspaces/shared-spaces/project/test/resources/test-image-2.jpg')
        response = self.client.get('/spaces/1/images')
        data = json.loads(response.data)

        self.assertTrue(are_images_same(
            data[0], '/workspaces/shared-spaces/project/test/resources/test-image-1.jpg'))
        self.assertTrue(are_images_same(
            data[1], '/workspaces/shared-spaces/project/test/resources/test-image-2.jpg'))

        self.client.delete('/spaces/1')

    def test_space_not_exist(self):
        register_and_login(self.client, 'usr')
        response = self.client.get('/spaces/999/images')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_not_member(self):
        create_space_as_not_member(self.client)
        response = self.client.get('/spaces/1/images')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')

    def test_no_images(self):
        create_space_as_admin(self.client, 'space-1')
        response = self.client.get('/spaces/1/images')
        expected_data = []
        data = json.loads(response.data)
        self.assertEqual(data, expected_data)

    def test_is_temp_bucket_created(self):
        self.assertTrue(find_bucket('shared-spaces-temp'))
