import json
from unittest import TestCase
from test.helper import register_and_login,  delete_all_records_from_db, client, logout, login, register
from test.test_create_space import create_space
from test.test_add_member import add_member


class TestDeleteSpace(TestCase):

    def setUp(self):
        delete_all_records_from_db()

    def test_not_logged_in(self):
        response = client.delete('/spaces/1')
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        register_and_login('usr')
        create_space("space-1")
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

    def test_not_member(self):
        register_and_login('other-usr')
        create_space('other-space')
        logout()
        register_and_login('usr')

        response = client.delete('/spaces/1')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')

    def test_not_admin(self):
        register('usr')
        register_and_login('admin')
        create_space('space')
        add_member(1, 1)
        logout()
        login('usr')

        response = client.delete('/spaces/1')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User not admin')

    def test_not_empty(self):
        register('usr')
        register_and_login('admin')
        create_space('space')
        add_member(1, 1)

        response = client.delete('/spaces/1')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'Space not empty')
