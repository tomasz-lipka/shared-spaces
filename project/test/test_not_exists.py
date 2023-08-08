from unittest import TestCase
from test.helper import register_and_login,  delete_all_records_from_db, client, register, create_space, login, logout


class TestAdmin(TestCase):

    def setUp(self):
        delete_all_records_from_db()
        register_and_login("usr")

    # ------------ SPACE TESTS ------------

    def test_get_space_not_exists(self):
        response = client.get('/spaces/999')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_rename_space_not_exists(self):
        data = {
            "new-name": "space_new_name"
        }
        response = client.put('/spaces/999', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_delete_space_not_exists(self):
        response = client.delete('/spaces/999')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    # ------------ MEMBER TESTS ------------

    def test_add_member_not_exists(self):
        logout()
        register('member')
        login('usr')
        create_space("space-1")

        data = {
            "user-id": "999"
        }
        response = client.post('/spaces/1/members', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"User with ID '999' doesn't exist")

    def test_add_member_to_space_not_exists(self):
        logout()
        register('member')
        login('usr')
        create_space("space-1")

        data = {
            "user-id": "2"
        }
        response = client.post('/spaces/999/members', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")
