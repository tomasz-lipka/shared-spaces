from sqlalchemy import Column, Integer, String
from base import Base


class User (Base):

    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)

    def __init__(self, email):
        self.email = email
