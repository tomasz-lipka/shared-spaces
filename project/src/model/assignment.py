"""
Module containing the Assignment model class.
"""
from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..model.base import Base


class Assignment(Base):
    """
    Model class representing the assignment entity.

    This class defines the structure of the Assignment entity, which represents the assignment
    of users to their respective spaces and grants admin roles within those spaces.
    """
    __tablename__ = 'assignments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    space_id = Column(Integer, ForeignKey('spaces.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_admin = Column(Boolean, default=False)

    space = relationship('Space')
    user = relationship('User')

    def __init__(self, space_id, user_id):
        self.space_id = space_id
        self.user_id = user_id

    def spaces_to_dict(self):
        """
        Convert an Assignment object to a dictionary representation.
        Returns:
            dict: A dictionary containing 'space' and 'is_admin' information.
        """
        return {
            'space': self.space.to_dict(),
            'is_admin': self.is_admin
        }

    def users_to_dict(self):
        """
        Convert an Assignment object to a dictionary representation.
        Returns:
            dict: A dictionary containing 'user' and 'is_admin' information.
        """
        return {
            'user': self.user.to_dict(),
            'is_admin': self.is_admin
        }

    __table_args__ = {"sqlite_autoincrement": True}
