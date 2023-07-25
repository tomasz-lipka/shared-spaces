import sys
sys.path.insert(1, '/workspaces/shared-spaces/project/src/model')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from connector import Connector
from base import Base


class SQLAlchemyConnector(Connector):
    """Connector to the database. Derives from the Connector base class
    """
    
    def connect(self):
        """Implementation of base class method. Connect to database"""
        return create_engine('sqlite:///my_db.sqlite')


    def create_schema(self, connection):
        """Implementation of base class method. Create schema in the database"""
        Base.metadata.create_all(connection)


    def establish_session(self, connection):
        """Implementation of base class method. Returns the session """
        Session = sessionmaker(bind=connection)
        return Session()

 