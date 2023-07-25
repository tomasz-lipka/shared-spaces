from sqlalchemy import Column, Integer, String
from base import Base


class User(Base):
    """
    Model of the user entity
    """
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)

    def __init__(self, email):
        self.email = email

    def __str__(self):
        return f"User(user_id='{self.user_id}', email={self.email})"

