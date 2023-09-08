"""
Module containing the TokenBlocklist model class.
"""
from sqlalchemy import Column, Integer, String
from ..model.base import Base


class TokenBlocklist(Base):
    """
    This class defines the structure of the TokenBlocklist.
    It keeps track who revoked a JWT token.
    'jti'' stands for JWTs unique identifier
    For more info check: https://flask-jwt-extended.readthedocs.io/en/stable/blocklist_and_token_revoking.html
    """
    __tablename__ = 'tokenblocklist'

    id = Column(Integer, primary_key=True, autoincrement=True)
    jti = Column(String(36), nullable=False, index=True)

    def __init__(self, jti):
        self.jti = jti
