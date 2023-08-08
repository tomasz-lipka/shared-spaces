import json
from unittest import TestCase
from test.helper import register_and_login, create_space, delete_all_records_from_db, client, create_space_by_other_user


class TestSpaceController(TestCase):

    def setUp(self):
        delete_all_records_from_db()
        register_and_login("usr")

    def test_basic_space_crud(self):
        self.create_space()
        self.get_space()
        self.rename_space()
        self.delete_space()
        self.get_space_not_exists()

    def create_space(self):
        response = create_space("space-1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Space created")

    def get_space(self):
        response = client.get('/spaces/1')
        expected_data = {
            "id": 1,
            "name": "space-1"
        }
        data = json.loads(response.data)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def rename_space(self):
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
        response = client.delete('/spaces/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Space deleted")

    def get_space_not_exists(self):
        response = client.get('/spaces/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '1' doesn't exist")

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

   
    def test_get_space_where_not_member(self):
        create_space_by_other_user("space-1")

        register_and_login("this-usr")
        response = client.get('/spaces/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"User-space pair doesn\'t exist")


    # def test_delete_space_where_only_member(self)