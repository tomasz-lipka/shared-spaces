import json
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
        register_and_login(self.client, 'admin-1')
        create_space(self.client, 'space-1')
        create_share(self.client, 1)
        logout(self.client)

        register(self.client, 'member-1')

        register_and_login(self.client, 'admin-2')
        create_space(self.client, 'space-2')
        create_share(self.client, 2)
        add_member(self.client, 2, 2)
        logout(self.client)

        login(self.client, 'member-1')
        create_share(self.client, 2)

        response = self.client.get('/spaces/2/shares')
        expected_data = [
            {
                "id": 2,
                "user": {
                    "id": 3,
                    "login": "admin-2"
                },
                "text": "Lorem ipsum",
                # "timestamp":
                "image_url": None
            },
            {
                "id": 3,
                "text": "Lorem ipsum",
                "user": {
                    "id": 2,
                    "login": "member-1"
                },
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
        register_and_login(self.client, 'usr')
        response = self.client.get('/spaces/999/shares')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_not_member(self):
        create_space_as_not_member(self.client)
        response = self.client.get('/spaces/1/shares')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')

    def test_normal_run_with_image(self):
        create_space_as_admin(self.client, 'space-1')
        create_share_with_image(
            self.client, 1, '/workspaces/shared-spaces/project/test/resources/test-image-1.jpg')
        create_share_with_image(
            self.client, 1, '/workspaces/shared-spaces/project/test/resources/test-image-2.jpg')
        create_share(self.client, 1)

        response = self.client.get('/spaces/1/shares')
        expected_data = [
            {
                "id": 1,
                "user": {
                    "id": 1,
                    "login": "admin"
                },
                "text": "Lorem ipsum",
                # "timestamp":
                # "image_url":
            },
            {
                "id": 2,
                "text": "Lorem ipsum",
                "user": {
                    "id": 1,
                    "login": "admin"
                },
                # "timestamp":
                # "image_url":
            },
            {
                "id": 3,
                "text": "Lorem ipsum",
                "user": {
                    "id": 1,
                    "login": "admin"
                },
                # "timestamp":
                "image_url": None
            }
        ]
        data = json.loads(response.data)

        self.assertTrue(are_images_same(
            data[0], '/workspaces/shared-spaces/project/test/resources/test-image-1.jpg'))

        self.assertTrue(are_images_same(
            data[1], '/workspaces/shared-spaces/project/test/resources/test-image-2.jpg'))

        data[0].pop("image_url", None)
        data[1].pop("image_url", None)
        for item in data:
            item.pop("timestamp", None)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

        self.client.delete('/spaces/1')
