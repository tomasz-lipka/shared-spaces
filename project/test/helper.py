import os
from flask_login import LoginManager
from sqlalchemy import MetaData, Table, text

from src.repository.sql_alchemy_repository import SqlAlchemyRepository, engine
from src.model.user import User
from app import create_app


def set_up_flask():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return SqlAlchemyRepository().get_by_id(User, user_id)

    return client


client = set_up_flask()


def delete_all_records_from_db():
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Get a list of all tables in the database
    table_names = metadata.tables.keys()

    # Delete all records from each table
    with engine.begin() as connection:
        for table_name in table_names:
            table = Table(table_name, metadata, autoload=True)
            connection.execute(table.delete())


def register(usr_login):
    data = {
        "login": usr_login,
        "password": "pwd",
        "confirm-password": "pwd"
    }
    return client.post('/register', json=data)


def login(usr_login):
    data = {
        "login": usr_login,
        "password": "pwd"
    }
    return client.post('/login', json=data)


def register_and_login(usr_login):
    register(usr_login)
    return login(usr_login)


def create_space(name):
    data = {
        "name": name
    }
    return client.post('/spaces', json=data)


def create_space_by_other_user(space_name):
    register_and_login("other-usr")
    create_space(space_name)
    client.get('/logout')
