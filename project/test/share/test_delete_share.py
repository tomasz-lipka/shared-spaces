import json
from unittest import TestCase
from test.helper import delete_all_records_from_db, client, create_space_as_admin, create_share, logout, register_and_login
# OK

class TestDeleteShare(TestCase):

    def setUp(self):
        delete_all_records_from_db()

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
