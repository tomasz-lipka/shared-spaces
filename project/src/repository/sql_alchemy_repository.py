"""
Module containing the SqlAlchemyRepository class.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..repository.repository import Repository
from ..model.base import Base
from ..model.user import User
from ..model.space import Space
from ..model.assignment import Assignment
from ..model.share import Share


engine = create_engine('sqlite:///test_db.sqlite')

# Creates schema in database
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class SqlAlchemyRepository(Repository):
    """
    Concrete implementation of the Repository abstract class using SQLAlchemy.
    This class provides methods for adding, deleting, and retrieving objects 
    from a database using SQLAlchemy.
    """

    def add(self, obj):
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj.id

    def delete_by_id(self, model, obj_id):
        """
        Implementation of the respective repository abstract class method.
        """
        obj = self.get_by_id(model, obj_id)
        if obj:
            session.delete(obj)
            session.commit()

    def get_by_id(self, model, obj_id):
        """
        Implementation of the respective repository abstract class method.
        """
        return session.get(model, obj_id)

    def get_first_by_filter(self, model, query_filter):
        """
        Implementation of the respective repository abstract class method.
        """
        return session.query(model).filter(query_filter).first()

    def get_first_by_two_filters(self, model, query_filter1, query_filter2):
        """
        Implementation of the respective repository abstract class method.
        """
        return session.query(model).filter(query_filter1).filter(query_filter2).first()

    def get_all_by_filter(self, model, query_filter):
        """
        Implementation of the respective repository abstract class method.
        """
        return session.query(model).filter(query_filter).all()
