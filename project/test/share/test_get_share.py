import json
from unittest import TestCase
from test.helper import (
    set_up, client, create_space_as_admin,
    create_share, register_and_login, logout,
    delete_all_buckets, create_share_with_image,
    create_space, register, login, add_member
)


class TestGetShare(TestCase):

    def setUp(self):
        set_up()

    def test_not_logged_in(self):
        response = client.get('/shares/1')
        self.assertEqual(response.status_code, 401)

    def test_normal_run_no_image(self):
        create_space_as_admin('space-1')
        response = create_share(1)
        response = client.get('/shares/1')
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
            "media_url": None
        }
        data = json.loads(response.data)
        data.pop("timestamp", None)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_not_exist(self):
        register_and_login('usr')
        response = client.get('/shares/999')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'No such share')

    def test_not_owned(self):
        create_space_as_admin('space-1')
        create_share(1)
        logout()
        register_and_login('usr')
        response = client.get('/shares/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User doesn\'t own this share')

    def test_normal_run_with_image(self):    
        create_space_as_admin('space-1')
        create_share_with_image(1)
        create_space('space-2')
        logout()
        register('usr')
        login('admin')
        add_member(2, 2)
        logout()
        login('usr')
        create_share_with_image(2)
        create_share_with_image(2)

        response = client.get('/shares/3')
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
            # "media_url":
        }
        data = json.loads(response.data)
    
        self.assertIn('https://', data["media_url"])
        self.assertIn('.s3.amazonaws.co', data["media_url"])
        self.assertIn('space-id-2', data["media_url"])
        self.assertIn('3.jpg', data["media_url"])
        
        data.pop("timestamp", None)
        data.pop("media_url", None)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

        delete_all_buckets()

