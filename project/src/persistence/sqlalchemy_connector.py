from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.base import Base


class SQLAlchemyConnector():
    """Connector to the database
    """
    
    def connect(self):
        """Connect to database"""
        return create_engine('sqlite:///my_db.sqlite')


    def create_schema(self, connection):
        """Create schema in the database"""
        Base.metadata.create_all(connection)


    def establish_session(self, connection):
        """Returns the session"""
        Session = sessionmaker(bind=connection)
        return Session()
    