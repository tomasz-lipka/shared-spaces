import json
from unittest import TestCase
from flask_login import LoginManager

from src.repository.sql_alchemy_repository import SqlAlchemyRepository
from src.model.user import User
from app import create_app


class AssignmentControllerTestCase(TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        login_manager = LoginManager()
        login_manager.init_app(self.app)

        @login_manager.user_loader
        def load_user(user_id):
            """Request loader according to Flask-Login library"""
            return SqlAlchemyRepository().get_by_id(User, user_id)

    def register(self):
        data = {
            "login": "test_user",
            "password": "pwd",
            "confirm-password": "pwd"
        }
        self.client.post('/register', json=data)

    def login(self):
        data = {
            "login": "test_user",
            "password": "pwd"
        }
        self.client.post('/login', json=data)

    def test_get_spaces(self):
        self.register()
        self.login()

        response = self.client.get('/spaces')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        expected_data = []
        self.assertEqual(data, expected_data)


if __name__ == '__main__':
    import pytest
    pytest.main()
