from sqlalchemy import Column, Integer, String
from ..model.base import Base


class Space(Base):
    """
    Model of the space entity
    """
    __tablename__ = 'spaces'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        """Returns dictionary for json serialization"""
        return {
            'id': self.id,
            'name': self.name
        }
