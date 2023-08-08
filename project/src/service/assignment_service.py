from flask_login import current_user, login_required

from ..repository.sql_alchemy_repository import SqlAlchemyRepository
from ..model.assignment import Assignment
from ..service.validator_helper import validate_user, validate_space, validate_assignment, validate_admin, validate_no_assignment
from ..exception.service_exception import ServiceException

repository = SqlAlchemyRepository()


@login_required
def get_users_assignments():
    """
    Gets all Assignments of logged in user. Shows where he's admin
    Returns: list(Assignment)
    """
    return repository.get_all_by_filter(Assignment, Assignment.user_id == current_user.get_id())


@login_required
def get_assignments_by_space_id(space_id):
    """
    Returns assignments by space_id
    Logged in user must be: member
    Returns: list(Assignments)
    """
    user = validate_user(current_user.get_id())
    space = validate_space(space_id)
    validate_assignment(user, space)
    return repository.get_all_by_filter(Assignment, Assignment.space_id == space.id)


@login_required
def create_assignment(user_id, space_id):
    """
    Creates Assignment. Assignment with given space_id and user_id musn't exist. User and Space must exist
    Logged in user must be: member, admin
    Returns: nothing
    """
    space = validate_space(space_id)
    admin_assignment = validate_assignment(
        validate_user(current_user.get_id()), space)
    validate_admin(admin_assignment)
    validate_no_assignment(validate_user(user_id), space)

    repository.add(Assignment(user_id, space_id))


@login_required
def delete_assignment_by_user_id_space_id(space_id, user_id):
    space = validate_space(space_id)
    admin_assignment = validate_assignment(
        validate_user(current_user.get_id()), space)
    validate_admin(admin_assignment)
    assignment = validate_assignment(validate_user(user_id), space)

    repository.delete_by_id(Assignment, assignment.id)


def create_assignment_with_admin(space_id):
    """
    Creates a new Assignment. Grants admin role to logged in user
    Returns: nothing
    """
    assignment = Assignment(current_user.get_id(), space_id)
    assignment.is_admin = True
    repository.add(assignment)


def delete_assignment(assignment):
    """
    Deletes assignment
    Returns: nothing
    """
    repository.delete_by_id(Assignment, assignment.id)


def change_admin_permission(space_id, user_id, is_admin):
    space = validate_space(space_id)
    admin_assignment = validate_assignment(
        validate_user(current_user.get_id()), space)
    validate_admin(admin_assignment)
    assignment = validate_assignment(validate_user(user_id), space)
    if not isinstance(is_admin, bool):
        raise ServiceException('"is admin" must be type boolean')
    
    assignment.is_admin = is_admin
    repository.add(assignment)
