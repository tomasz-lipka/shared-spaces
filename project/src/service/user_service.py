"""
Module for managing user authentication and related actions.

This module provides functions for user authentication, user creation, password management, 
and user retrieval. It handles login, logout, changing passwords, creating users, 
verifying passwords, and retrieving user objects. The module works with Flask-Login 
for authentication and uses bcrypt for password hashing.
"""
import bcrypt
from flask_login import login_user, logout_user, current_user, login_required

from ..repository.sql_alchemy_repository import SqlAlchemyRepository
from ..exception.service_exception import ServiceException
from ..model.user import User


repository = SqlAlchemyRepository()


def login(user_login, password):
    """
    Log in a user using provided credentials.
    Args:
        user_login (str): User's login identifier.
        password (str): User's password.
    """
    if current_user.is_authenticated:
        raise ServiceException('Already logged in')
    user = get_verified_user(user_login, password)
    if not user:
        raise ServiceException('Wrong login and/or password')
    login_user(user)


def create_user(user_login, password, confirm_password):
    """
    Create a new user with provided credentials.
    Args:
        user_login (str): User's desired login identifier (e.g., username or email).
        password (str): User's password.
        confirm_password (str): Confirmation of the user's password.
    """
    if current_user.is_authenticated:
        raise ServiceException('Already logged in')
    if password != confirm_password:
        raise ServiceException('Passwords don\'t match')
    if repository.get_first_by_filter(User, User.login == user_login):
        raise ServiceException('User already exists')
    repository.add(User(user_login, get_hashed(password)))


def logout():
    """
    Log out the currently logged-in user.
    """
    logout_user()


@login_required
def change_password(old_password, new_password, confirm_password):
    """
    Change the password of the currently logged-in user.
    Args:
        old_password (str): User's current password.
        new_password (str): User's new desired password.
        confirm_password (str): Confirmation of the new password.
    """
    session_user = repository.get_by_id(User, current_user.get_id())
    if not verify_password(session_user, old_password):
        raise ServiceException('Wrong password')
    if new_password != confirm_password:
        raise ServiceException('New passwords don\'t match')
    session_user.password = get_hashed(new_password)
    repository.add(session_user)


def get_verified_user(user_login, password):
    """
    Get a verified user based on provided login credentials.
    Args:
        user_login (str): User's login identifier.
        password (str): User's password.
    """
    user = repository.get_first_by_filter(User, User.login == user_login)
    if user and verify_password(user, password):
        return user
    return None


def get_hashed(password):
    """
    Get the hashed version of a password using bcrypt.
    Args:
        password (str): The password to be hashed.
    Returns:
        bytes: The hashed password.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def verify_password(user, password):
    """
    Verify if a provided password matches the hashed password of a user.
    Args:
        user (User): The user object containing the hashed password.
        password (str): The password to be verified.
    Returns:
        bool: True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), user.password)


def get_user_by_user_id(user_id):
    """
    Retrieve a user by their ID.
    Args:
        user_id (int): ID of the target user.
    Returns:
        User: The user object.
    """
    return repository.get_by_id(User, user_id)
