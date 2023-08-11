"""
Module containing the Space model class.
"""
from sqlalchemy import Column, Integer, String
from ..model.base import Base


class Space(Base):
    """
    Model class representing individual spaces.
    This class defines the structure of the Space entity.
    """
    __tablename__ = 'spaces'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        """
        Convert a Space object to a dictionary representation.
        Returns:
            dict: A dictionary containing 'id' and 'name' information.
        """
        return {
            'id': self.id,
            'name': self.name
        }
