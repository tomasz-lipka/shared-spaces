import json
from unittest import TestCase
from test.helper import (
    get_app, logout, purge_db, create_space_as_admin,
    create_share, register_and_login, create_share_with_image,
    create_space, register, login, add_member, find_bucket, are_images_same,
    WRONG_TOKEN
)


class TestGetShare(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_not_logged_in(self):
        response = self.client.get(
            '/shares/1', headers={"Authorization": f"Bearer {WRONG_TOKEN}"})
        self.assertEqual(
            response.data, b'{"msg":"Signature verification failed"}\n')
        self.assertEqual(response.status_code, 422)

    def test_normal_run(self):
        token = create_space_as_admin(self.client, 'space-1')
        create_share(self.client, 1, token)
        response = self.client.get(
            '/shares/1', headers={"Authorization": f"Bearer {token}"})
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
            "text": "Lorem ipsum",
            # "timestamp":
            "image_url": None
        }
        data = json.loads(response.data)
        data.pop("timestamp", None)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_not_exist(self):
        token = register_and_login(self.client, 'usr')
        response = self.client.get(
            '/shares/999', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b'No such share')

    def test_not_owned(self):
        token = create_space_as_admin(self.client, 'space-1')
        create_share(self.client, 1, token)
        logout(self.client)
        token = register_and_login(self.client, 'usr')
        response = self.client.get(
            '/shares/1', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User doesn\'t own this share')

    def test_normal_run_with_image(self):
        token = create_space_as_admin(self.client, 'space-1')
        create_share_with_image(
            self.client, 1, '/workspaces/shared-spaces/project/test/resources/test-image-1.jpg', token)
        create_space(self.client, 'space-2', token)
        logout(self.client)
        register(self.client, 'usr')
        token = login(self.client, 'admin')
        add_member(self.client, 2, 2, token)
        logout(self.client)
        token = login(self.client, 'usr')
        create_share_with_image(
            self.client, 2, '/workspaces/shared-spaces/project/test/resources/test-image-2.jpg', token)
        create_share_with_image(
            self.client, 2, '/workspaces/shared-spaces/project/test/resources/test-image-3.jpg', token)

        response = self.client.get(
            '/shares/3', headers={"Authorization": f"Bearer {token}"})
        expected_data = {
            "id": 3,
            "space": {
                "id": 2,
                "name": "space-2"
            },
            "user": {
                "id": 2,
                "login": "usr"
            },
            "text": "Lorem ipsum"
            # "timestamp":
            # "image_url":
        }
        data = json.loads(response.data)

        self.assertTrue(are_images_same(
            data, '/workspaces/shared-spaces/project/test/resources/test-image-3.jpg'))

        data.pop("timestamp", None)
        data.pop("image_url", None)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

        logout(self.client)
        token = login(self.client, 'admin')
        self.client.delete('/spaces/2/members/2',
                           headers={"Authorization": f"Bearer {token}"})
        self.client.delete(
            '/spaces/1', headers={"Authorization": f"Bearer {token}"})
        self.client.delete(
            '/spaces/2', headers={"Authorization": f"Bearer {token}"})

    def test_not_owned_with_image(self):
        token = create_space_as_admin(self.client, 'space-1')
        create_share_with_image(
            self.client, 1, '/workspaces/shared-spaces/project/test/resources/test-image-1.jpg', token)
        logout(self.client)
        token = register_and_login(self.client, 'usr')
        response = self.client.get(
            '/shares/1', headers={"Authorization": f"Bearer {token}"})

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User doesn\'t own this share')
        self.assertTrue(find_bucket('test-space-id-1'))

        logout(self.client)
        token = login(self.client, 'admin')
        self.client.delete(
            '/spaces/1', headers={"Authorization": f"Bearer {token}"})
