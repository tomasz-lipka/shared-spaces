import json
from unittest import TestCase
from test.helper import register_and_login,  delete_all_records_from_db, client, logout, register
from test.test_create_space import create_space


def add_member(space_id, user_id):
    data = {
        "user-id": user_id
    }
    return client.post(f'/spaces/{space_id}/members', json=data)


class TestRenameSpace(TestCase):

    def setUp(self):
        delete_all_records_from_db()

    def test_not_logged_in(self):
        response = add_member(1, 1)
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        register('usr')
        register_and_login('admin')
        create_space("space-1")
        response = add_member(1, 1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Member added")


    # def test_space_not_exist(self):
    
    # def test_member_not_exist(self):

    # def test_not_member(self):


    # def test_not_admin(self):

    # def test_payload_invalid_type

    def test_wrong_json_key(self):
        register('usr')
        register_and_login('admin')
        create_space("space-1")
        data = {
            "wrong": 1
        }
        response = client.post('/spaces/1/members', json=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload :'user-id'")