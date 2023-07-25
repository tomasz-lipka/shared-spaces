import sys
sys.path.insert(1, '/workspaces/shared-spaces/project/src/exception')
sys.path.insert(1, '/workspaces/shared-spaces/project/src/persistence')
sys.path.insert(1, '/workspaces/shared-spaces/project/src/model')

from repository_exception import RepositoryException
from sqlalchemy_connector import SQLAlchemyConnector
from post import Post


connector = SQLAlchemyConnector()

connection = connector.connect()
connector.create_schema(connection)
session = connector.establish_session(connection)


def create_post(user_id, text):
    """Creates a new post in the persistence layer"""
    if not get_post_by_text(text):
        post = Post(user_id, text)
        session.add(post)
        session.commit()
    else:
        raise RepositoryException('User already exists')


# def get_all_users():
#     """Returns all users from the persistence layer"""
#     return session.query(User).all()


def get_post_by_text(text):
    """Returns the first found post from persistence layer by the given text"""
    # return session.query(User).filter(User.email==email).first()
    return False
   