import bcrypt
from flask_login import login_user, logout_user, current_user, login_required

from repository.sql_alchemy_repository import SqlAlchemyRepository
from exception.service_exception import ServiceException
from model.user import User


repository = SqlAlchemyRepository()


def login(login, password):
    """Logs user in"""
    user = get_verified_user(login, password)
    if not user:
        raise ServiceException('Wrong login and/or password')
    login_user(user)


def create_user(login, password, confirm_password):
    """Creates a new user"""
    if password != confirm_password:
        raise ServiceException('Passwords don\'t match')
    if repository.get_first_by_filter(User, User.login == login):
        raise ServiceException('User already exists')
    repository.add(User(login, get_hashed(password)))


def logout():
    """Logs the current user out"""
    logout_user()


@login_required
def change_password(old_password, new_password, confirm_password):
    """Changes the exisiting password to a new one"""
    session_user = repository.get_by_id(User, current_user.get_id())
    if not verify_password(session_user, old_password):
        raise ServiceException('Wrong password')
    if new_password != confirm_password:
        raise ServiceException('New passwords don\'t match')
    session_user.password = get_hashed(new_password)
    repository.add(session_user)


def get_verified_user(login, password):
    """Verifies if the given credentials match an exisiting user"""
    user = repository.get_first_by_filter(User, User.login == login)
    if user and verify_password(user, password):
        return user
    return None


def get_hashed(password):
    """Returns the hashed password according to hashing algorithm"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def verify_password(user, password):
    """Checks if the users hashed password matches the input password"""
    return bcrypt.checkpw(password.encode('utf-8'), user.password)


def get_user_by_user_id(user_id):
    """
    Gets user by user_id
    Returns: User
    """
    return repository.get_by_id(User, user_id)