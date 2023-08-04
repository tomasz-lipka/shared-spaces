from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from ..model.base import Base


class Share(Base):
    """
    Model of the share entity
    """
    __tablename__ = 'shares'

    id = Column(Integer, primary_key=True, autoincrement=True)
    space_id = Column(Integer, ForeignKey('spaces.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    text = Column(String, nullable=False)
    timestamp = Column(DateTime, default=func.now())

    user = relationship('User')
    space = relationship('Space')

    def __init__(self, space_id, user_id, text):
        self.space_id = space_id
        self.user_id = user_id
        self.text = text

    def __str__(self):
        return f"Share(id='{self.id}', space={self.space}, user={self.user}, text={self.text}, timestamp={self.timestamp})"

    def to_dict(self):
        """Returns dictionary for json serialization"""
        return {
            'id': self.id,
            'space': self.space.to_dict(),
            'user': self.user.to_dict(),
            'text': self.text,
            'timestamp': self.timestamp.isoformat()
        }
