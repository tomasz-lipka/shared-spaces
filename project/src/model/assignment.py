from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..model.base import Base


class Assignment(Base):
    """
    Model of the assignment entity. It assigns users to their spaces and grants admin roles
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
        """Returns dictionary for json serialization"""
        return {
            'space': self.space.to_dict(),
            'is_admin': self.is_admin
        }

    def users_to_dict(self):
        """Returns dictionary for json serialization"""
        return {
            'user': self.user.to_dict(),
            'is_admin': self.is_admin
        }
