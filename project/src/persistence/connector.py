from abc import ABC, abstractmethod

class Connector(ABC):
    """Abstract class defining methods to connect and interact with the persistence layer"""


    @abstractmethod
    def connect(self):
        """Connecting to persistence layer"""


    @abstractmethod
    def create_schema(self, connection):
        """Creating schema in persistence layer"""


    @abstractmethod
    def establish_session(self, connection):
        """Establishing session to interact with persistence layer"""
    
