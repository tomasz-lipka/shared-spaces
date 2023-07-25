import sys
sys.path.insert(1, '/workspaces/shared-spaces/project/src/exception')
sys.path.insert(1, '/workspaces/shared-spaces/project/src/persistence')
sys.path.insert(1, '/workspaces/shared-spaces/project/src/model')

from repository_exception import RepositoryException
from sqlalchemy_connector import SQLAlchemyConnector
from space import Space


connector = SQLAlchemyConnector()

connection = connector.connect()
connector.create_schema(connection)
session = connector.establish_session(connection)


def create_space(name):
    """Creates a new space in the persistence layer"""
    space = Space(name)
    session.add(space)
    session.commit()


# def get_all_users():
#     """Returns all users from the persistence layer"""
#     return session.query(User).all()


# def get_user_by_email(email):
#     """Returns the first found user from persistence layer by the given parameter"""
#     return session.query(User).filter(User.email==email).first()
   