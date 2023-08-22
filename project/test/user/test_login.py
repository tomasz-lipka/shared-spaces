from unittest import TestCase
from test.helper import set_up, client, login, register, register_and_login


class TestLogin(TestCase):

    def setUp(self):
        set_up()

    def test_normal_run(self):
        response = register_and_login("usr")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Logged in")

    def test_wrong_login(self):
        response = login('wrong_login')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, b"Wrong login and/or password")

    def test_wrong_pwd(self):
        register('usr')
        data = {
            "login": "usr",
            "password": "wrong_pwd"
        }
        response = client.post('/login', json=data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, b"Wrong login and/or password")

    def test_login_and_logout(self):
        register_and_login("usr")
        response = client.get('/logout')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Logged out")

    def test_wrong_json_key_login(self):
        register('usr')
        data = {
            "wrong": "usr",
            "password": "wrong_pwd"
        }
        response = client.post('/login', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'login'")

    def test_wrong_json_key_password(self):
        register('usr')
        data = {
            "login": "usr",
            "wrong": "wrong_pwd"
        }
        response = client.post('/login', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'password'")

    def test_when_already_logged_in(self):
        register_and_login('usr')
        response = login('usr')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, b'Already logged in')

    def test_when_already_logged_in_other_usr(self):
        register('other-usr')
        register_and_login('usr')
        response = login('other-usr')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, b'Already logged in')
