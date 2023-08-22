from unittest import TestCase
from test.helper import (
    set_up, client, create_space_as_admin,
    create_share, logout, register_and_login,
    create_share_with_image, find_bucket, delete_all_buckets
)


class TestDeleteShare(TestCase):

    def setUp(self):
        set_up()

    def test_not_logged_in(self):
        response = client.delete('/shares/1')
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        create_space_as_admin('space-1')
        create_share(1)
        response = client.delete('/shares/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Share deleted")

        response = client.get('/shares/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'No such share')

    def test_not_owned(self):
        create_space_as_admin('space-1')
        create_share(1)
        logout()
        register_and_login('usr')

        response = client.delete('/shares/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User doesn\'t own this share')

    def test_not_exist(self):
        register_and_login('usr')
        response = client.delete('/shares/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'No such share')

    def test_not_owned_with_image(self):
        create_space_as_admin('space-1')
        create_share_with_image(1)
        logout()
        register_and_login('usr')

        response = client.delete('/shares/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User doesn\'t own this share')
        self.assertTrue(find_bucket('space-id-1'))

        delete_all_buckets()
