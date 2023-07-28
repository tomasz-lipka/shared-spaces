from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from repository.repository import Repository
from model.base import Base
from model.user import User
from model.space import Space
from model.member import Member


engine = create_engine('sqlite:///my_db.sqlite')

# Creates schema in database
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class SqlAlchemyRepository(Repository):
    """Implementation of the Repository abstract class"""

    def add(self, object):
        """Add or update entity in repo and return its ID"""
        session.add(object)
        session.commit()
        session.refresh(object)
        return object.id

    def delete(self, object):
        """Delete entity from repo"""
        pass

    def get_by_id(self, model, id):
        """Get entity of given model from repo by id"""
        return session.query(model).get(id)

    def get_first_by_filter(self, model, query_filter):
        """Get first found entity of given model using a query filter"""
        return session.query(model).filter(query_filter).first()

    def get_all_by_filter(self, model, query_filter):
        """Get all found entities of given model using a query filter"""
        return session.query(model).filter(query_filter).all()

    def get_all(self, oreference_object):
        """Get all entities associated to a given reference object"""
        pass
