from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from base import Base


class Post(Base):
    """
    Model of the post entity
    """
    __tablename__ = 'posts'

    post_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    text = Column(String, nullable=False, unique=True)
    timestamp = Column(DateTime, default=func.now())

    # Define the relationship between User and Post
    user = relationship("User", backref="Post")


    def __init__(self, user_id, text):
        self.user_id = user_id
        self.text = text


    def __str__(self):  
        return f"Post(post_id='{self.post_id}', user_id={self.user_id}, text={self.text}, timestamp={self.timestamp}, user={self.user})"
