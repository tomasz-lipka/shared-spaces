"""
Module containing the UserService class.
"""
import bcrypt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from injector import inject

from ...exception.service.service_exception import ServiceException
from ...exception.service.unauthorized_exception import UnauthorizedException
from ...repository.repository import Repository
from ..helper.service_validator import ServiceValidator
from ..helper.input_validator import validate_usr_input
from ...model.user import User
from ...model.tockenblocklist import TokenBlocklist


class UserService():
    """
    This module provides methods for user authentication, user creation, password management, 
    and user retrieval. It handles login, logout, changing passwords, creating users, 
    verifying passwords, and retrieving user objects. The module works with Flask-JWT-Extended 
    for authentication, uses bcrypt for password hashing and utilizes validation methods.
    """

    MAX_PASSWORD_LEN = 99999

    @inject
    def __init__(self, repository: Repository, validator: ServiceValidator):
        self.repository = repository
        self.validator = validator

    def login(self, user_login, password):
        """
        Log in a user using provided credentials.
        Args:
            user_login (str): User's login identifier.
            password (str): User's password.
        """
        self.validator.validate_not_null(user_login, 'Login')
        self.validator.validate_not_null(password, 'Password')
        user = self.__get_verified_user(user_login, password)
        if not user:
            raise UnauthorizedException('Wrong login and/or password')
        return create_access_token(identity=user.login)

    def create_user(self, user_login, password, confirm_password):
        """
        Create a new user with provided credentials.
        Args:
            user_login (str): User's desired login identifier (e.g., username or email).
            password (str): User's password.
            confirm_password (str): Confirmation of the user's password.
        """
        self.validator.validate_not_null(user_login, 'Login')
        self.validator.validate_not_null(password, 'Password')
        self.validator.validate_not_null(confirm_password, 'Confirm password')
        validate_usr_input(user_login, 'Login', 15)
        validate_usr_input(password, 'Password', self.MAX_PASSWORD_LEN)
        if password != confirm_password:
            raise ServiceException('Passwords don\'t match', 400)
        if self.repository.get_first_by_filter(User, User.login == user_login):
            raise ServiceException('User already exists', 400)
        self.repository.add(User(user_login, self.__get_hashed(password)))
        return self.validator.validate_user_by_login(user_login)

    @jwt_required()
    def logout(self):
        """
        Log out the currently logged-in user.
        """
        jti = get_jwt()["jti"]
        self.repository.add(TokenBlocklist(jti))

    @jwt_required()
    def change_password(self, old_password, new_password, confirm_password):
        """
        Change the password of the currently logged-in user.
        Args:
            old_password (str): User's current password.
            new_password (str): User's new desired password.
            confirm_password (str): Confirmation of the new password.
        """
        self.validator.validate_not_null(old_password, 'Old password')
        self.validator.validate_not_null(new_password, 'New password')
        self.validator.validate_not_null(confirm_password, 'Confirm password')
        validate_usr_input(new_password, 'New password', self.MAX_PASSWORD_LEN)
        session_user = self.repository.get_by_id(
            User, self.validator.get_logged_in_user_id())
        if not self.__verify_password(session_user, old_password):
            raise UnauthorizedException('Wrong password')
        if new_password != confirm_password:
            raise ServiceException('New passwords don\'t match', 400)
        session_user.password = self.__get_hashed(new_password)
        self.repository.add(session_user)

    def __get_verified_user(self, user_login, password):
        user = self.repository.get_first_by_filter(
            User, User.login == user_login)
        if user and self.__verify_password(user, password):
            return user
        return None

    def __get_hashed(self, password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def __verify_password(self, user, password):
        return bcrypt.checkpw(password.encode('utf-8'), user.password)
