from model.user import User
from persistence.sqlalchemy_connector import SQLAlchemyConnector
from exception.repository_exception import RepositoryException


sql_alchemy_connector = SQLAlchemyConnector()

connection = sql_alchemy_connector.connect()
sql_alchemy_connector.create_schema(connection)
session = sql_alchemy_connector.establish_session(connection)


def create_user(user):
    """Creates a new user in the persistence layer"""
    if not get_user_by_login(user.login):
        session.add(user)
        session.commit()
    else:
        raise RepositoryException('User already exists')


def get_user_by_login(login):
    """Returns the first found user from persistence layer by the given parameter"""
    return session.query(User).filter(User.login == login).first()


def get_user_by_id(user_id):
    """Returns the user by a given id"""
    return session.query(User).get(user_id)


def update_user(user):
    """Updates a user in the database"""
    session.add(user)
    session.commit()
