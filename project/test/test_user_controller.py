import json
from unittest import TestCase
from flask_login import LoginManager

from src.repository.sql_alchemy_repository import SqlAlchemyRepository
from src.model.user import User
from app import create_app
from test.test_helper import delete_db_file


class TestUserController(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

        login_manager = LoginManager()
        login_manager.init_app(cls.app)

        @login_manager.user_loader
        def load_user(user_id):
            return SqlAlchemyRepository().get_by_id(User, user_id)

    def test_registration_pwd_not_same(cls):
        data = {
            "login": "test_registration_pwd_not_same",
            "password": "pwd",
            "confirm-password": "other_pwd"
        }
        response = cls.client.post('/register', json=data)
        cls.assertEqual(response.status_code, 400)
        cls.assertEqual(response.data, b"Passwords don\'t match")

    def test_registration_user_already_exists(cls):
        data = {
            "login": "test_registration_user_already_exists",
            "password": "pwd",
            "confirm-password": "pwd"
        }
        response = cls.client.post('/register', json=data)
        data = {
            "login": "test_registration_user_already_exists",
            "password": "pwd",
            "confirm-password": "pwd"
        }
        response = cls.client.post('/register', json=data)
        cls.assertEqual(response.status_code, 400)
        cls.assertEqual(response.data, b"User already exists")

    def test_proper_registration(cls):
        data = {
            "login": "test_proper_registration",
            "password": "pwd",
            "confirm-password": "pwd"
        }
        response = cls.client.post('/register', json=data)
        cls.assertEqual(response.status_code, 200)
        cls.assertEqual(response.data, b"User created")

    def test_wrong_login(cls):
        data = {
            "login": "test_wrong_login",
            "password": "pwd"
        }
        response = cls.client.post('/login', json=data)
        cls.assertEqual(response.status_code, 401)
        cls.assertEqual(response.data, b"Wrong login and/or password")

    def test_wrong_pwd(cls):
        data = {
            "login": "test_wrong_pwd",
            "password": "pwd",
            "confirm-password": "pwd"
        }
        cls.client.post('/register', json=data)
        data = {
            "login": "test_wrong_pwd",
            "password": "wrong_pwd"
        }
        response = cls.client.post('/login', json=data)
        cls.assertEqual(response.status_code, 401)
        cls.assertEqual(response.data, b"Wrong login and/or password")

    def test_login_and_logout(cls):
        data = {
            "login": "test_login_and_logout",
            "password": "pwd",
            "confirm-password": "pwd"
        }
        cls.client.post('/register', json=data)
        data = {
            "login": "test_login_and_logout",
            "password": "pwd"
        }
        cls.client.post('/login', json=data)
        response = cls.client.get('/logout')
        cls.assertEqual(response.status_code, 200)
        cls.assertEqual(response.data, b"Logged out")

    @classmethod
    def tearDownClass(cls):
        delete_db_file()
