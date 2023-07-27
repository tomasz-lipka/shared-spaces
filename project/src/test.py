from abc import ABC, abstractmethod


class Repository(ABC):
    """Abstract repository class. Template for specific repository implementations"""

    @abstractmethod
    def add(self, object):
        """Add or update entity in repo"""

    @abstractmethod
    def delete(self, object):
        """Delete entity from repo"""

    @abstractmethod
    def get_by_id(self, model, id):
        """Get entity of given model from repo by id"""

    @abstractmethod
    def get_by_filter(self, model, query_filter):
        """Get entity of given model using a query filter"""

    @abstractmethod
    def get_all(self, reference_object):
        """Get all entities associated to a given reference object"""


class SqlAlchemyRepository(Repository):
    """Implementation of the Repository abstract class"""

    def add(self, object):
        """Add or update entity in repo"""
        pass

    def delete(self, object):
        """Delete entity from repo"""
        pass

    def get_by_id(self, model, id):
        """Get entity of given model from repo by id"""
        pass

    def get_by_filter(self, model, query_filter):
        """Get entity of given model using a query filter"""
        pass

    # def get_all(self, oreference_object):
    #     """Get all entities associated to a given reference object"""
    #     pass


repo = SqlAlchemyRepository()
