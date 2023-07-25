from sqlalchemy import Column, Integer, String
from base import Base


class Space(Base):
    """
    Model of the space entity
    """
    __tablename__ = 'spaces'

    space_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Space(space_id='{self.space_id}', name={self.name})"

