import sys
sys.path.insert(1, '/workspaces/shared-spaces/project/src/exception')
sys.path.insert(1, '/workspaces/shared-spaces/project/src/persistence')
sys.path.insert(1, '/workspaces/shared-spaces/project/src/model')

from repository_exception import RepositoryException
from sqlalchemy_connector import SQLAlchemyConnector
from space_assignment import SpaceAssignment


connector = SQLAlchemyConnector()

connection = connector.connect()
connector.create_schema(connection)
session = connector.establish_session(connection)


def create_space_assignment(user_id, space_id):
    """Creates a new space assignment in the persistence layer"""
    space_assignment = SpaceAssignment(user_id, space_id)
    session.add(space_assignment)
    session.commit()


# def get_all_users():
#     """Returns all users from the persistence layer"""
#     return session.query(User).all()


# def get_user_by_email(email):
#     """Returns the first found user from persistence layer by the given parameter"""
#     return session.query(User).filter(User.email==email).first()
   