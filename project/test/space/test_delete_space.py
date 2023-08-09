import json
from unittest import TestCase
from test.helper import register_and_login, set_up, client, create_space_as_admin, create_space_as_member, add_member, register


class TestDeleteSpace(TestCase):

    def setUp(self):
        set_up()

    def test_not_logged_in(self):
        response = client.delete('/spaces/1')
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        create_space_as_admin('space-1')
        response = client.delete('/spaces/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Space deleted")

        response = client.get('/spaces/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '1' doesn't exist")

    def test_not_exist(self):
        register_and_login('usr')
        response = client.delete('/spaces/999')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_not_admin(self):
        create_space_as_member('space-1')
        response = client.delete('/spaces/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User not admin')

    def test_not_empty(self):
        register('member')
        create_space_as_admin('space-1')
        add_member(1, 1)
        response = client.delete('/spaces/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'Space not empty')
