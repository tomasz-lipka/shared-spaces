"""
Module containing the Repository abstract class.
"""
from abc import ABC, abstractmethod


class Repository(ABC):
    """
    Abstract repository class. Template for specific repository implementations.
    This class defines an abstract repository interface with methods
    for interacting with a database.
    """

    @abstractmethod
    def __init__(self, repository_url):
        """
        Initialize a Repository instance.
        Args:
            repository_url (str): The URL to the repository.
        """

    @abstractmethod
    def add(self, obj):
        """
         Abstract method to add or update an object to the database.
         Args:
             obj: The object to be added to the database
         """

    @abstractmethod
    def delete_by_id(self, model, obj_id):
        """
        Abstract method to delete an object from the database by its ID.
        Args:
            obj_id: The ID of the object to be deleted.
        """

    @abstractmethod
    def get_by_id(self, model, obj_id):
        """
        Abstract method to retrieve an object from the database by its ID.
        Args:
            model: The model class representing the type of object to be retrieved.
            obj_id: The ID of the object to be retrieved.
        Returns:
            object: The retrieved object.
        """

    @abstractmethod
    def get_first_by_filter(self, model, query_filter):
        """
        Abstract method to retrieve the first object from the database based on a filter.
        Args:
            model: The model class representing the type of object to be retrieved.
            query_filter: The filter condition for the query.
        Returns:
            object: The retrieved object.
        """

    @abstractmethod
    def get_first_by_two_filters(self, model, query_filter1, query_filter2):
        """
        Abstract method to retrieve the first object from the database based on two filters.
        Args:
            model: The model class representing the type of object to be retrieved.
            query_filter1: The first filter condition for the query.
            query_filter2: The second filter condition for the query.
        Returns:
            object: The retrieved object.
        """

    @abstractmethod
    def get_all_by_filter(self, model, query_filter):
        """
        Abstract method to retrieve all objects from the database based on a filter.
        Args:
            model: The model class representing the type of objects to be retrieved.
            query_filter: The filter condition for the query.
        Returns:
            list: A list of retrieved objects.
        """

    @abstractmethod
    def get_all_by_two_filters(self, model, query_filter1, query_filter2):
        """
        Abstract method to retrieve all objects from the database based on two filters.
        Args:
            model: The model class representing the type of object to be retrieved.
            query_filter1: The first filter condition for the query.
            query_filter2: The second filter condition for the query.
        Returns:
            list: A list of retrieved objects.
        """

    @abstractmethod
    def create_schema(self):
        """
        Create a schema according to the model entities. 
        Defines the data structure and relationships.
        """
