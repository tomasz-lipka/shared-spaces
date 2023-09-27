import json
import time
from unittest import TestCase
from test.helper import (
    get_app, logout, purge_db, create_share, register_and_login, create_space,
    register, add_member, login, create_space_as_not_member,
    create_space_as_admin, create_share_with_image, are_images_same
)


class TestGetShares(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_not_logged_in(self):
        response = self.client.get('/spaces/1/shares')
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        token = register_and_login(self.client, 'admin-1')
        create_space(self.client, 'space-1', token)
        create_share(self.client, 1, token)
        logout(self.client)

        register(self.client, 'member-1')

        token = register_and_login(self.client, 'admin-2')
        create_space(self.client, 'space-2', token)
        create_share(self.client, 2, token)
        time.sleep(0.5)
        add_member(self.client, 2, 2, token)
        logout(self.client)

        token = login(self.client, 'member-1')
        create_share(self.client, 2, token)
        time.sleep(0.5)

        response = self.client.get(
            '/spaces/2/shares', headers={"Authorization": f"Bearer {token}"})
        expected_data = [
            {
                "id": 3,
                "user": {
                    "id": 2,
                    "login": "member-1"
                },
                "text": "Lorem ipsum",
                # "timestamp":
                "image_url": None
            },
            {
                "id": 2,
                "user": {
                    "id": 3,
                    "login": "admin-2"
                },
                "text": "Lorem ipsum",
                # "timestamp":
                "image_url": None
            }
        ]
        data = json.loads(response.data)
        for item in data:
            item.pop("timestamp", None)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_space_not_exist(self):
        token = register_and_login(self.client, 'usr')
        response = self.client.get(
            '/spaces/999/shares', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_not_member(self):
        token = create_space_as_not_member(self.client)
        response = self.client.get(
            '/spaces/1/shares', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')

    def test_normal_run_with_image(self):
        token = create_space_as_admin(self.client, 'space-1')
        create_share_with_image(
            self.client, 1, 'test-image-1.jpg', token)
        time.sleep(0.5)
        create_share_with_image(
            self.client, 1, 'test-image-2.jpg', token)
        time.sleep(0.5)
        create_share(self.client, 1, token)
        time.sleep(0.5)

        response = self.client.get(
            '/spaces/1/shares', headers={"Authorization": f"Bearer {token}"})
        expected_data = [
            {
                "id": 3,
                "user": {
                    "id": 1,
                    "login": "admin"
                },
                "text": "Lorem ipsum",
                # "timestamp":
                "image_url": None
            },
            {
                "id": 2,
                "user": {
                    "id": 1,
                    "login": "admin"
                },
                "text": "Lorem ipsum",
                # "timestamp":
                # "image_url":
            },
            {
                "id": 1,
                "user": {
                    "id": 1,
                    "login": "admin"
                },
                "text": "Lorem ipsum",
                # "timestamp":
                # "image_url":
            }
        ]
        data = json.loads(response.data)

        self.assertTrue(are_images_same(
            data[2], 'test-image-1.jpg'))

        self.assertTrue(are_images_same(
            data[1], 'test-image-2.jpg'))

        data[1].pop("image_url", None)
        data[2].pop("image_url", None)
        for item in data:
            item.pop("timestamp", None)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

        self.client.delete(
            '/spaces/1', headers={"Authorization": f"Bearer {token}"})
