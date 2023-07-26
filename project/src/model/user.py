from flask_login import UserMixin
from sqlalchemy import Column, Integer, String
from model.base import Base


class User(Base, UserMixin):
    """
    Model of the user entity
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def __str__(self):
        return f"User(id='{self.id}', login={self.login}, password={self.password})"
