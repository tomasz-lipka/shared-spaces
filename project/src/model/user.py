"""
Module containing the User model class.
"""
from sqlalchemy import Column, Integer, String
from ..model.base import Base


class User(Base):
    """
    Model class representing individual users.
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def to_dict(self):
        """
        Convert an User object to a dictionary representation.
        Returns:
            dict: A dictionary containing 'id' and 'login' information.
        """
        return {
            'id': self.id,
            'login': self.login
        }
