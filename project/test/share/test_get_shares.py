import json
from unittest import TestCase
from test.helper import (
    set_up, client, create_share, logout, register_and_login, create_space,
    register, add_member, login, create_space_as_not_member,
    delete_all_buckets, create_space_as_admin, create_share_with_image
)


class TestGetShares(TestCase):

    def setUp(self):
        set_up()

    def test_not_logged_in(self):
        response = client.get('/spaces/1/shares')
        self.assertEqual(response.status_code, 401)

    def test_normal_run_no_image(self):
        register_and_login('admin-1')
        create_space('space-1')
        create_share(1)
        logout()

        register('member-1')

        register_and_login('admin-2')
        create_space('space-2')
        create_share(2)
        add_member(2, 2)
        logout()

        login('member-1')
        create_share(2)

        response = client.get('/spaces/2/shares')
        expected_data = [
            {
                "id": 2,
                "user": {
                    "id": 3,
                    "login": "admin-2"
                },
                "text": "Lorem ipsum",
                # "timestamp":
                "media_url": None
            },
            {
                "id": 3,
                "text": "Lorem ipsum",
                "user": {
                    "id": 2,
                    "login": "member-1"
                },
                # "timestamp":
                "media_url": None
            }
        ]
        data = json.loads(response.data)
        for item in data:
            item.pop("timestamp", None)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_space_not_exist(self):
        register_and_login('usr')
        response = client.get('/spaces/999/shares')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_not_member(self):
        create_space_as_not_member()
        response = client.get('/spaces/1/shares')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')

    def test_normal_run_with_image(self):
        create_space_as_admin('space-1')
        create_share_with_image(1)
        create_share_with_image(1)

        response = client.get('/spaces/1/shares')
        expected_data = [
            {
                "id": 1,
                "user": {
                    "id": 1,
                    "login": "admin"
                },
                "text": "Lorem ipsum",
                # "timestamp":
                # "media_url":
            },
            {
                "id": 2,
                "text": "Lorem ipsum",
                "user": {
                    "id": 1,
                    "login": "admin"
                },
                # "timestamp":
                # "media_url":
            }
        ]
        data = json.loads(response.data)

        self.assertIn('https://', data[0]["media_url"])
        self.assertIn('.s3.amazonaws.co', data[0]["media_url"])
        self.assertIn('space-id-1', data[0]["media_url"])
        self.assertIn('1.jpg', data[0]["media_url"])

        self.assertIn('https://', data[1]["media_url"])
        self.assertIn('.s3.amazonaws.co', data[1]["media_url"])
        self.assertIn('space-id-1', data[1]["media_url"])
        self.assertIn('2.jpg', data[1]["media_url"])

        for item in data:
            item.pop("timestamp", None)
            item.pop("media_url", None)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

        delete_all_buckets()
