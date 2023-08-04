from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..repository.repository import Repository
from ..model.base import Base
from ..model.user import User
from ..model.space import Space
from ..model.assignment import Assignment
from ..model.share import Share


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

    def delete_by_id(self, model, id):
        """Deletes an entity from repo by ID"""
        object = self.get_by_id(model, id)
        if object:
            session.delete(object)
            session.commit()

    def get_by_id(self, model, id):
        """Returns an entity of given model from repo by id"""
        return session.query(model).get(id)

    def get_first_by_filter(self, model, query_filter):
        """Returns first found entity of given model using a query filter"""
        return session.query(model).filter(query_filter).first()

    def get_first_by_two_filters(self, model, query_filter1, query_filter2):
        """Returns first found entity of given model using two query filters"""
        return session.query(model).filter(query_filter1).filter(query_filter2).first()

    def get_all_by_filter(self, model, query_filter):
        """Returns all found entities of given model using a query filter"""
        return session.query(model).filter(query_filter).all()

    def get_all(self, reference_object):
        """Returns all entities associated to a given reference object"""
        pass
