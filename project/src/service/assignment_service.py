from repository.sql_alchemy_repository import SqlAlchemyRepository
from flask_login import current_user, login_required
from model.assignment import Assignment
from exception.service_exception import ServiceException


repository = SqlAlchemyRepository()


@login_required
def get_all():
    """
    Gets all Assignments. Shows where logged in user has admin role
    Logged in user must be member
    Returns: list(Assignment)
    """
    return repository.get_all_by_filter(Assignment, Assignment.user_id == current_user.get_id())


@login_required
def create(user_id, space_id):
    """
    Creates a new Assignment. Grants admin role to logged in user
    Returns: nothing
    """
    assignment = Assignment(user_id, space_id)
    assignment.is_admin = True
    repository.add(assignment)


@login_required
def get_all_by_space_id(space_id):
    """
    Returns assignments by space_id.
    Logged in user must be member
    Returns: list(Assignments)
    """
    if not is_member(current_user.get_id(), space_id):
        raise ServiceException(
            'User not member of requested space or no such space')
    return repository.get_all_by_filter(Assignment, Assignment.space_id == space_id)


# def delete_by_space_id(user_id, space_id):
#     """Deletes entity by space ID if there is only the admin member"""
#     if is_empty_by_space_id(user_id, space_id):
#         repository.delete_by_id(Assignment, space_id)

def is_admin(space_id):
    """
    Checks if logged in user is admin of given space
    Returns: boolean
    """
    pass


def is_empty(user_id, space_id):
    pass


def is_member(user_id, space_id):
    """
    Checks if given user is member of given space
    Returns: boolean
    """
    assignments = repository.get_all_by_filter(
        Assignment, Assignment.user_id == user_id)
    for assignment in assignments:
        if assignment.space_id == space_id:
            return True
