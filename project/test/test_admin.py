import json
from unittest import TestCase
from test.helper import register_and_login, register, create_space, delete_all_records_from_db, client, login, logout


class TestAdmin(TestCase):

    def setUp(self):
        delete_all_records_from_db()
        register_and_login("admin")

    # ------------ SPACE TESTS ------------

    def test_create_space(self):
        response = create_space("space-1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Space created")

    def test_get_space(self):
        create_space("space-1")
        response = client.get('/spaces/1')
        expected_data = {
            "id": 1,
            "name": "space-1"
        }
        data = json.loads(response.data)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_get_spaces(self):
        create_space("space-1")
        create_space("space-2")
        response = client.get('/spaces')
        expected_data = [
            {
                "is_admin": True,
                "space": {
                    "id": 1,
                    "name": "space-1"
                }
            },
            {
                "is_admin": True,
                "space": {
                    "id": 2,
                    "name": "space-2"
                }
            }
        ]
        data = json.loads(response.data)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_rename_space(self):
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

    def delete_space(self):
        create_space("space-1")
        response = client.delete('/spaces/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Space deleted")

        response = client.get('/spaces/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '1' doesn't exist")

    # ------------ MEMBER TESTS ------------

    def test_add_member(self):
        logout()
        register('member')
        login('admin')
        create_space("space-1")

        data = {
            "user-id": 2
        }
        response = client.post('/spaces/1/members', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Member added")

    

    # add member already added

    # def test_get_members(self):

    # def test_delete_member(self):

    # def test_make_admin(self):

    # def test_unmake_admin(self):

        # ------------ SHARE TESTS ------------
