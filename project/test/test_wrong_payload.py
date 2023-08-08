import json
from unittest import TestCase
from test.helper import register_and_login, register, create_space, delete_all_records_from_db, client, login, logout


class TestAdmin(TestCase):

    def setUp(self):
        delete_all_records_from_db()
        register_and_login("usr")

# ------------ SPACE TESTS ------------

# ------------ MEMBER TESTS ------------


def test_add_member(self):
    logout()
    register('member')
    login('admin')
    create_space("space-1")

    data = {
        "user-id": "WRONG"
    }
    response = client.post('/spaces/1/members', json=data)
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.data, b"User with ID 'WRONG' doesn't exist")
