import bcrypt
import repository.generic_repository as repository
from exception.service_exception import ServiceException
from model.user import User


def create_user(login, password, confirm_password):
    """Creates a new user"""
    if password == confirm_password:
        user = User(login, get_hashed(password))
    else:
        raise ServiceException('Passwords don\'t match')
    if not repository.get_by_filter(User, User.login == login):
        repository.add(user)
    else:
        raise ServiceException('User already exists')


def get_verified_user(login, password):
    """Verifies if the given credentials match an exisiting user"""
    user = repository.get_by_filter(User, User.login == login)
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

# TODO
def change_password(new_password):
    """Changes the exisiting hashed password to a new one"""
    # self.password = self.get_hashed(new_password)
