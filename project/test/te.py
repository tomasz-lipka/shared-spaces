from unittest import TestCase
from test.helper import set_up, client, register, register_and_login, logout, create_space_as_admin, create_share

from flask_login import current_user

class TestRegistration(TestCase):

    def setUp(self):
        logout()
        set_up()

    def test_tes(self):
        create_space_as_admin('space-1')
        create_share(1)
        logout()
        register_and_login('usr')
        response = client.get('/shares/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User doesn\'t own this share')
