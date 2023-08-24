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


class SqlAlchemyRepository(Repository):
    """
    Concrete implementation of the Repository abstract class using SQLAlchemy.
    This class provides methods for adding, deleting, and retrieving objects 
    from a database using SQLAlchemy.
    """

    def __init__(self, repository_url):
        self.engine = create_engine(repository_url)
        self.__create_schema(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add(self, obj):
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj.id

    def delete_by_id(self, model, obj_id):
        """
        Implementation of the respective repository abstract class method.
        """
        obj = self.get_by_id(model, obj_id)
        if obj:
            self.session.delete(obj)
            self.session.commit()

    def get_by_id(self, model, obj_id):
        """
        Implementation of the respective repository abstract class method.
        """
        return self.session.get(model, obj_id)

    def get_first_by_filter(self, model, query_filter):
        """
        Implementation of the respective repository abstract class method.
        """
        return self.session.query(model).filter(query_filter).first()

    def get_first_by_two_filters(self, model, query_filter1, query_filter2):
        """
        Implementation of the respective repository abstract class method.
        """
        return self.session.query(model).filter(query_filter1).filter(query_filter2).first()

    def get_all_by_filter(self, model, query_filter):
        """
        Implementation of the respective repository abstract class method.
        """
        return self.session.query(model).filter(query_filter).all()

    def __create_schema(self, engine):
        Base.metadata.create_all(engine)
