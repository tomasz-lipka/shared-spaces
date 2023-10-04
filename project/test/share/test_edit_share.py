import json
from unittest import TestCase
from test.helper import (
    get_app, logout, purge_db, create_space_as_admin,
    edit_share_with_image, create_share, register_and_login,
    create_share_with_image, are_images_same, login, WRONG_TOKEN
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
        token, space_id, admin = create_space_as_admin(self.client, 'space-1')
        _, share_id = create_share(self.client, space_id, token)
        data = {
            "text": "Edit lorem ipsum"
        }
        response = self.client.put(
            f'/shares/{share_id}', data=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Share edited")

        response = self.client.get(
            f'/shares/{share_id}', headers={"Authorization": f"Bearer {token}"})
        expected_data = {
            "id": share_id,
            "space": {
                "id": space_id,
                "name": "space-1"
            },
            # "timestamp":,
            "user": {
                "id": admin.get('id'),
                "login": admin.get('login')
            },
            "text": "Edit lorem ipsum",
            "image_url": None
        }
        data = json.loads(response.data)
        data.pop("timestamp", None)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_not_owned(self):
        token, space_id, _ = create_space_as_admin(self.client, 'space-1')
        _, share_id = create_share(self.client, space_id, token)
        logout(self.client)
        token, _ = register_and_login(self.client)

        data = {
            "text": "Edit lorem ipsum"
        }
        response = self.client.put(
            f'/shares/{share_id}', data=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User doesn\'t own this share')

    def test_not_exist(self):
        token, _ = register_and_login(self.client)
        data = {
            "text": "Edit lorem ipsum"
        }
        response = self.client.put(
            '/shares/999999999', data=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b'No such share')

    def test_wrong_json_key(self):
        token, space_id, _ = create_space_as_admin(self.client, 'space-1')
        _, share_id = create_share(self.client, space_id, token)
        data = {
            "wrong": "Edit lorem ipsum"
        }
        response = self.client.put(
            f'/shares/{share_id}', data=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Text must be provided")

    def test_not_logged_in_with_image(self):
        response = edit_share_with_image(
            self.client, 1, 'test-image-1.jpg', WRONG_TOKEN)
        self.assertEqual(
            response.data, b'{"msg":"Signature verification failed"}\n')
        self.assertEqual(response.status_code, 422)

    def test_normal_run_with_image(self):
        token, space_id, admin = create_space_as_admin(self.client, 'space-1')
        _, share_id = create_share_with_image(
            self.client, space_id, 'test-image-1.jpg', token)
        response = edit_share_with_image(
            self.client, share_id, 'test-image-2.jpg', token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Share edited")

        response = self.client.get(
            f'/shares/{share_id}', headers={"Authorization": f"Bearer {token}"})
        data = json.loads(response.data)
        self.assertTrue(are_images_same(
            data, 'test-image-2.jpg'))
        expected_data = {
            "id": share_id,
            "space": {
                "id": space_id,
                "name": "space-1"
            },
            # "timestamp":,
            "user": {
                "id": admin.get('id'),
                "login": admin.get('login')
            },
            "text": "Edit lorem ipsum",
            # "image_url":
        }
        data.pop("timestamp", None)
        data.pop("image_url", None)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

        self.client.delete(
            f'/spaces/{space_id}', headers={"Authorization": f"Bearer {token}"})

    def test_not_owned_with_image(self):
        token, space_id, admin = create_space_as_admin(self.client, 'space-1')
        _, share_id = create_share_with_image(
            self.client, space_id, 'test-image-1.jpg', token)
        logout(self.client)
        token, _ = register_and_login(self.client)

        response = edit_share_with_image(
            self.client, share_id, 'test-image-2.jpg', token)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User doesn\'t own this share')

        logout(self.client)
        token = login(self.client, admin.get('login'))
        self.client.delete(
            f'/spaces/{space_id}', headers={"Authorization": f"Bearer {token}"})

    def test_not_exist_with_image(self):
        token, _ = register_and_login(self.client)
        response = edit_share_with_image(
            self.client, 999999999, 'test-image-2.jpg', token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b'No such share')

    def test_null_json_value(self):
        token, space_id, _ = create_space_as_admin(self.client, 'space-1')
        _, share_id = create_share(self.client, space_id, token)
        data = {
            "text": None
        }
        response = self.client.put(
            f'/shares/{share_id}', data=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Text must be provided")

    def test_empty_text(self):
        token, _, _ = create_space_as_admin(self.client, 'space-1')
        _, share_id = create_share(self.client, 1, token)
        data = {
            "text": "   "
        }
        response = self.client.put(
            f'/shares/{share_id}', data=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Text cannot be empty")

    def test_min_char_text(self):
        token, _, _ = create_space_as_admin(self.client, 'space-1')
        _, share_id = create_share(self.client, 1, token)
        data = {
            "text": "a"
        }
        response = self.client.put(
            f'/shares/{share_id}', data=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Text min 3 characters")

    def test_max_char_text(self):
        token, _, _ = create_space_as_admin(self.client, 'space-1')
        _, share_id = create_share(self.client, 1, token)
        data = {
            "text": "text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text "
        }
        response = self.client.put(
            f'/shares/{share_id}', data=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Text max 200 characters")
