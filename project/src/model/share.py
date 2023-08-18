"""
Module containing the Share model class.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from ..model.base import Base


class Share(Base):
    """
    This class defines the structure of the Share entity,
    which represents shared content within spaces.
    """
    __tablename__ = 'shares'

    id = Column(Integer, primary_key=True, autoincrement=True)
    space_id = Column(Integer, ForeignKey('spaces.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    text = Column(String, nullable=False)
    timestamp = Column(DateTime, default=func.now())
    media_url = None

    user = relationship('User')
    space = relationship('Space')

    def __init__(self, space_id, user_id, text):
        self.space_id = space_id
        self.user_id = user_id
        self.text = text

    def to_dict(self):
        """
        Convert a Share object to a dictionary representation.
        Returns:
            dict: A dictionary containing share fields, 'space' and 'user' information.
        """
        return {
            'id': self.id,
            'space': self.space.to_dict(),
            'user': self.user.to_dict(),
            'text': self.text,
            'timestamp': self.timestamp.isoformat(),
            'media_url': self.media_url
        }

    def shares_to_dict(self):
        """
        Convert a Share object to a dictionary representation.
        Returns:
            dict: A dictionary containing share fields and 'user' information.
        """
        return {
            'id': self.id,
            'user': self.user.to_dict(),
            'text': self.text,
            'timestamp': self.timestamp.isoformat(),
            'media_url': self.media_url
        }
