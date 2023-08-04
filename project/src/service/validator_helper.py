from ..repository.sql_alchemy_repository import SqlAlchemyRepository
from ..model.user import User
from ..model.space import Space
from ..model.assignment import Assignment
from ..model.share import Share
from ..exception.service_exception import ServiceException

repository = SqlAlchemyRepository()


def validate_space(space_id):
    """
    Checks if given space exists
    Returns: Space
    """
    space = repository.get_by_id(Space, space_id)
    if not space:
        raise ServiceException(f"Space with ID '{space_id}' doesn't exist")
    return space


def validate_user(user_id):
    """
    Checks if given user exists
    Returns: User
    """
    user = repository.get_by_id(User, user_id)
    if not user:
        raise ServiceException(f"User with ID '{user_id}' doesn't exist")
    return user


def validate_assignment(user, space):
    """
    Checks if given user-space pair exists
    Returns: Assignment
    """
    assignment = repository.get_first_by_two_filters(
        Assignment, Assignment.user_id == user.id, Assignment.space_id == space.id)
    if not assignment:
        raise ServiceException('User-space pair doesn\'t exist')
    return assignment


def validate_no_assignment(user, space):
    """
    Checks if given user-space pair doesn't exists
    Returns: nothing
    """
    if repository.get_first_by_two_filters(Assignment, Assignment.user_id == user.id, Assignment.space_id == space.id):
        raise ServiceException('User-space pair already exists')


def validate_admin(assignment):
    """
    Checks if logged in user is admin of given assignment
    Returns: nothing
    """
    if not assignment.is_admin:
        raise ServiceException('User not admin')


def contains_only_owner(space):
    """
    Checks if space is empty (except owner himself)
    Returns: boolean
    """
    assignments = repository.get_all_by_filter(
        Assignment, Assignment.space_id == space.id)
    return len(assignments) == 1


def validate_share(share_id):
    share = repository.get_by_id(Share, share_id)
    if not share:
        raise ServiceException('No such share')
    return share


def validate_share_owner(share, user_id):
    if not share.user_id == user_id:
        raise ServiceException('User doesn\'t own this share')

