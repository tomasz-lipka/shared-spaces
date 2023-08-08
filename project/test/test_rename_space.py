import json
from unittest import TestCase
from test.helper import register_and_login,  delete_all_records_from_db, client, logout, login, register
from test.test_create_space import create_space
from test.test_add_member import add_member


class TestRenameSpace(TestCase):

    def setUp(self):
        delete_all_records_from_db()

    def test_not_logged_in(self):
        data = {
            "new-name": "space_new_name"
        }
        response = client.put('/spaces/1', json=data)
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        register_and_login('usr')
        create_space("space-1")
        data = {
            "new-name": "space_new_name"
        }
        response = client.put('/spaces/1', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Space renamed")

        response = client.get('/spaces/1')
        expected_data = {
            "id": 1,
            "name": "space_new_name"
        }
        data = json.loads(response.data)
        self.assertEqual(data, expected_data)

    def test_not_exist(self):
        register_and_login('usr')
        data = {
            "new-name": "space_new_name"
        }
        response = client.put('/spaces/999', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_not_member(self):
        register_and_login('other-usr')
        create_space('other-space')
        logout()
        register_and_login('usr')

        data = {
            "new-name": "space_new_name"
        }
        response = client.put('/spaces/1', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')

    def test_not_admin(self):
        register('usr')
        register_and_login('admin')
        create_space('space')
        add_member(1, 1)
        logout()
        login('usr')

        data = {
            "new-name": "space_new_name"
        }
        response = client.put('/spaces/1', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User not admin')

    def test_wrong_json_key(self):
        register_and_login('usr')
        create_space("space-1")
        data = {
            "wrong": "space_new_name"
        }
        response = client.put('/spaces/1', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload :'new-name'")
