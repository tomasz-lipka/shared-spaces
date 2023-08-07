import json
from unittest import TestCase
from flask_login import LoginManager

from src.repository.sql_alchemy_repository import SqlAlchemyRepository
from src.model.user import User
from app import create_app
from test.test_helper import delete_db_file, register_and_login


class TestSpaceController(TestCase):


    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        login_manager = LoginManager()
        login_manager.init_app(self.app)

        @login_manager.user_loader
        def load_user(user_id):
            return SqlAlchemyRepository().get_by_id(User, user_id)

   
    def test_space_endpoints(self):
        register_and_login(self.client)
        self.create_space()
        self.get_space()
        self.rename_space()
        self.delete_space()
        self.get_space_not_exists()

    def create_space(self):
        data = {
            "name": "test_create_space"
        }
        response = self.client.post('/spaces', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Space created")

    def get_space(self):
        response = self.client.get('/spaces/1')
        expected_data = {
            "id": 1,
            "name" : "test_create_space"
        }
        data = json.loads(response.data)
        self.assertEqual(data, expected_data)

    def rename_space(self):
        data = {
            "new-name": "space_new_name"
        }
        response = self.client.put('/spaces/1', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Space renamed")
        response = self.client.get('/spaces/1')
        expected_data = {
            "id": 1,
            "name" : "space_new_name"
        }
        data = json.loads(response.data)
        self.assertEqual(data, expected_data)


    def delete_space(self):
        response = self.client.delete('/spaces/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Space deleted")

    def get_space_not_exists(self):
        response = self.client.get('/spaces/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '1' doesn't exist")
    

    # ---

    rename_space_not_exists
    delete_space_not_exists

    # def test_get_all_my_spaces(self):

    # def test_rename_space_where_not_admin(self)

    # def test_get_space_where_not_member(self)

    # def test_delete_space_where_not_admin(self)

    # def test_get_only_spaces_where_member(self)

    # def test_delete_not_empty_space(self)

    # def test_try_access_endpoints_not_logged_in(self)
