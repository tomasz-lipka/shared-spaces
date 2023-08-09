from abc import ABC, abstractmethod


class Repository(ABC):
    """Abstract repository class. Template for specific repository implementations"""

    @abstractmethod
    def add(self, object):
        """Add or update entity in repo"""

    @abstractmethod
    def delete_by_id(self, id):
        """Deletes an entity from repo by ID"""

    @abstractmethod
    def get_by_id(self, model, id):
        """Returns an entity of given model from repo by id"""

    @abstractmethod
    def get_first_by_filter(self, model, query_filter):
        """Returns first found entity of given model using a query filter"""

    @abstractmethod
    def get_first_by_two_filters(self, model, query_filter1, query_filter2):
        """Returns first found entity of given model using two query filters"""

    @abstractmethod
    def get_all_by_filter(self, model, query_filter):
        """Returns all found entities of given model using a query filter"""
