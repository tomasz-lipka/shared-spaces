import json
from unittest import TestCase
from test.helper import (
    get_app, logout, purge_db, create_space_as_admin, register_and_login,
    create_share, create_space_as_not_member, create_share_with_image,
    find_bucket, WRONG_TOKEN
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
        response = create_share(self.client, 1, WRONG_TOKEN)
        self.assertEqual(
            response.data, b'{"msg":"Signature verification failed"}\n')
        self.assertEqual(response.status_code, 422)

    def test_normal_run(self):
        token = create_space_as_admin(self.client, 'space-1')
        response = create_share(self.client, 1, token)
        expected_data = {
            "id": 1,
            "space": {
                "id": 1,
                "name": "space-1"
            },
            "user": {
                "id": 1,
                "login": "admin"
            },
            "text": "Lorem ipsum"
            # "timestamp":
            # "image_url":
        }
        data = json.loads(response.data)
        data.pop("timestamp", None)
        data.pop("image_url", None)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_space_not_exist(self):
        token = register_and_login(self.client, 'admin')
        response = create_share(self.client, 999, token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_not_member(self):
        token = create_space_as_not_member(self.client)
        response = create_share(self.client, 1, token)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')

    def test_wrong_json_key(self):
        token = create_space_as_admin(self.client, 'space-1')
        data = {
            "wrong": "Lorem ipsum"
        }
        response = self.client.post(
            '/spaces/1/shares', data=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Text must be provided")

    def test_normal_run_with_image(self):
        token = create_space_as_admin(self.client, 'space-1')
        response = create_share_with_image(
            self.client, 1, 'test-image-1.jpg', token)
        self.assertEqual(response.status_code, 200)
        self.client.delete(
            '/spaces/1', headers={"Authorization": f"Bearer {token}"})

    def test_not_logged_in_with_image(self):
        response = create_share_with_image(
            self.client, 1, 'test-image-1.jpg', WRONG_TOKEN)
        self.assertEqual(
            response.data, b'{"msg":"Signature verification failed"}\n')
        self.assertEqual(response.status_code, 422)
        self.assertFalse(find_bucket('test-space-id-1'))

    def test_space_not_exist_with_image(self):
        token = register_and_login(self.client, 'admin')
        response = create_share_with_image(
            self.client, 999, 'test-image-1.jpg', token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")
        self.assertFalse(find_bucket('test-space-id-999'))

    def test_not_member_with_image(self):
        token = create_space_as_not_member(self.client)
        response = create_share_with_image(
            self.client, 1, 'test-image-1.jpg', token)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')
        self.assertFalse(find_bucket('test-space-id-1'))

    def test_null_json_value(self):
        token = create_space_as_admin(self.client, 'space-1')
        data = {
            "text": None
        }
        response = self.client.post(
            '/spaces/1/shares', data=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Text must be provided")

    def test_empty_text(self):
        token = create_space_as_admin(self.client, 'space-1')
        data = {
            "text": "    "
        }
        response = self.client.post(
            '/spaces/1/shares', data=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Text cannot be empty")

    def test_min_char_text(self):
        token = create_space_as_admin(self.client, 'space-1')
        data = {
            "text": "a"
        }
        response = self.client.post(
            '/spaces/1/shares', data=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Text min 3 characters")

    def test_max_char_text(self):
        token = create_space_as_admin(self.client, 'space-1')
        data = {
            "text": "text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text "
        }
        response = self.client.post(
            '/spaces/1/shares', data=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Text max 200 characters")
