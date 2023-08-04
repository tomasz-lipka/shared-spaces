import json
from unittest import TestCase, mock
from flask import Flask

from flask_login import LoginManager
import secrets

from src.controller.user_controller import user_controller
from src.controller.space_controller import space_controller
from src.controller.assignment_controller import assignment_controller
from src.controller.share_controller import share_controller
from src.repository.sql_alchemy_repository import SqlAlchemyRepository
from src.model.user import User


class AssignmentControllerTestCase(TestCase):
    def setUp(self):
        # Create a test Flask app and register the assignment_controller blueprint
        self.app = Flask(__name__)
        self.app.register_blueprint(user_controller)
        self.app.register_blueprint(space_controller)
        self.app.register_blueprint(assignment_controller)
        self.app.register_blueprint(share_controller)

        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        # Generates a 32-byte (64-character) random hex string
        self.app.config["SECRET_KEY"] = secrets.token_hex(32)

        login_manager = LoginManager()
        login_manager.init_app(self.app)


        @login_manager.user_loader
        def load_user(user_id):
            """Request loader according to Flask-Login library"""
            return SqlAlchemyRepository().get_by_id(User, user_id)


    def test_get_spaces(self):
    # Prepare the data to be sent in the POST request
        data = {
            "login":"tomtst",
            "password":"pwd",
            "confirm-password":"pwd"
        }
        self.client.post('/register', json=data)


        data2 = {
            "login":"tomtst",
            "password":"pwd"
        }
        self.client.post('/login', json=data2)
            
        # Make a request to the endpoint
        response = self.client.get('/spaces')

        # Assert the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Convert the JSON response to a Python list
        data = json.loads(response.data)

        # Assert the response contains the expected data
        expected_data = []
        self.assertEqual(data, expected_data)

if __name__ == '__main__':
    import pytest
    pytest.main()