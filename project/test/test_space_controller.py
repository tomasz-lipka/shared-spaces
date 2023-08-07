import json
from unittest import TestCase
from flask_login import LoginManager

from src.repository.sql_alchemy_repository import SqlAlchemyRepository
from src.model.user import User
from app import create_app
from test.test_helper import delete_db_file, register_and_login


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

        register_and_login(cls.client)

    # def test_create_space():

    # def test_get_space():

    # def test_rename_space():

    # def test_delete_space()

    # test_get_space_not_exists()

    # ---

    # def test_get_all_my_spaces():

    # def test_rename_space_where_not_admin

    # def test_get_space_where_not_member()

    # def test_delete_space_where_not_admin()

    # def test_get_only_spaces_where_member()

    # def test_delete_not_empty_space()

    # def test_try_access_endpoint_not_logged_in()


    @classmethod
    def tearDownClass(cls):
        delete_db_file()
