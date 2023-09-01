import json
from unittest import TestCase
from test.helper import (
    get_app, logout, purge_db, create_space_as_admin,
    edit_share_with_image, create_share, register_and_login,
    create_share_with_image, are_images_same, login
)


class TestEditShare(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_not_logged_in(self):
        data = {
            "text": "Edit lorem ipsum"
        }
        response = self.client.put('/shares/1', data=data)
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        create_space_as_admin(self.client, 'space-1')
        create_share(self.client, 1)
        data = {
            "text": "Edit lorem ipsum"
        }
        response = self.client.put('/shares/1', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Share edited")

        response = self.client.get('/shares/1')
        expected_data = {
            "id": 1,
            "space": {
                "id": 1,
                "name": "space-1"
            },
            # "timestamp":,
            "user": {
                "id": 1,
                "login": "admin"
            },
            "text": "Edit lorem ipsum",
            "image_url": None
        }
        data = json.loads(response.data)
        data.pop("timestamp", None)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_not_owned(self):
        create_space_as_admin(self.client, 'space-1')
        create_share(self.client, 1)
        logout(self.client)
        register_and_login(self.client, 'usr')

        data = {
            "text": "Edit lorem ipsum"
        }
        response = self.client.put('/shares/1', data=data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User doesn\'t own this share')

    def test_not_exist(self):
        register_and_login(self.client, 'usr')
        data = {
            "text": "Edit lorem ipsum"
        }
        response = self.client.put('/shares/1', data=data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b'No such share')

    def test_wrong_json_key(self):
        create_space_as_admin(self.client, 'space-1')
        create_share(self.client, 1)
        data = {
            "wrong": "Edit lorem ipsum"
        }
        response = self.client.put('/shares/1', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Text must be provided")

    def test_not_logged_in_with_image(self):
        response = edit_share_with_image(
            self.client, 1, '/workspaces/shared-spaces/project/test/resources/test-image-1.jpg')
        self.assertEqual(response.status_code, 401)

    def test_normal_run_with_image(self):
        create_space_as_admin(self.client, 'space-1')
        create_share_with_image(
            self.client, 1, '/workspaces/shared-spaces/project/test/resources/test-image-1.jpg')
        response = edit_share_with_image(
            self.client, 1, '/workspaces/shared-spaces/project/test/resources/test-image-2.jpg')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Share edited")

        response = self.client.get('/shares/1')
        data = json.loads(response.data)
        self.assertTrue(are_images_same(
            data, '/workspaces/shared-spaces/project/test/resources/test-image-2.jpg'))
        expected_data = {
            "id": 1,
            "space": {
                "id": 1,
                "name": "space-1"
            },
            # "timestamp":,
            "user": {
                "id": 1,
                "login": "admin"
            },
            "text": "Edit lorem ipsum",
            # "image_url":
        }
        data.pop("timestamp", None)
        data.pop("image_url", None)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

        self.client.delete('/spaces/1')

    def test_not_owned_with_image(self):
        create_space_as_admin(self.client, 'space-1')
        create_share_with_image(
            self.client, 1, '/workspaces/shared-spaces/project/test/resources/test-image-1.jpg')
        logout(self.client)
        register_and_login(self.client, 'usr')

        response = edit_share_with_image(
            self.client, 1, '/workspaces/shared-spaces/project/test/resources/test-image-2.jpg')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User doesn\'t own this share')

        logout(self.client)
        login(self.client, 'admin')
        self.client.delete('/spaces/1')

    def test_not_exist_with_image(self):
        register_and_login(self.client, 'usr')
        response = edit_share_with_image(
            self.client, 1, '/workspaces/shared-spaces/project/test/resources/test-image-2.jpg')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b'No such share')

    def test_null_json_value(self):
        create_space_as_admin(self.client, 'space-1')
        create_share(self.client, 1)
        data = {
            "text": None
        }
        response = self.client.put('/shares/1', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Text must be provided")

    def test_empty_text(self):
        create_space_as_admin(self.client, 'space-1')
        create_share(self.client, 1)
        data = {
            "text": "   "
        }
        response = self.client.put('/shares/1', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Text cannot be empty")

    def test_min_char_text(self):
        create_space_as_admin(self.client, 'space-1')
        create_share(self.client, 1)
        data = {
            "text": "a"
        }
        response = self.client.put('/shares/1', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Text min 3 characters")

    def test_max_char_text(self):
        create_space_as_admin(self.client, 'space-1')
        create_share(self.client, 1)
        data = {
            "text": "text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text "
        }
        response = self.client.put('/shares/1', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Text max 200 characters")
