from unittest import TestCase
from test.helper import (
    get_app, logout, purge_db, create_space_as_admin, register_and_login,
    create_share, create_space_as_not_member, create_share_with_image,
    find_bucket
)


class TestCreateShare(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_not_logged_in(self):
        response = create_share(self.client, 1)
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        create_space_as_admin(self.client, 'space-1')
        response = create_share(self.client, 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Share created")

    def test_space_not_exist(self):
        register_and_login(self.client, 'admin')
        response = create_share(self.client, 999)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_not_member(self):
        create_space_as_not_member(self.client)
        response = create_share(self.client, 1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')

    def test_wrong_json_key(self):
        create_space_as_admin(self.client, 'space-1')
        data = {
            "wrong": "Lorem ipsum"
        }
        response = self.client.post('/spaces/1/shares', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'text'")

    def test_normal_run_with_image(self):
        create_space_as_admin(self.client, 'space-1')
        response = create_share_with_image(
            self.client, 1, '/workspaces/shared-spaces/project/test/resources/test-image-1.jpg')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Share with image created")
        self.client.delete('/spaces/1')

    def test_not_logged_in_with_image(self):
        response = create_share_with_image(
            self.client, 1, '/workspaces/shared-spaces/project/test/resources/test-image-1.jpg')
        self.assertEqual(response.status_code, 401)
        self.assertFalse(find_bucket('test-space-id-1'))

    def test_space_not_exist_with_image(self):
        register_and_login(self.client, 'admin')
        response = create_share_with_image(
            self.client, 999, '/workspaces/shared-spaces/project/test/resources/test-image-1.jpg')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")
        self.assertFalse(find_bucket('test-space-id-999'))

    def test_not_member_with_image(self):
        create_space_as_not_member(self.client)
        response = create_share_with_image(
            self.client, 1, '/workspaces/shared-spaces/project/test/resources/test-image-1.jpg')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')
        self.assertFalse(find_bucket('test-space-id-1'))
