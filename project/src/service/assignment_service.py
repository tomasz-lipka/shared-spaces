"""
Module containing functions for managing assignments and permissions of space-user pairs.

This module includes functions for fetching, creating, modifying, and deleting user assignments
and their associated permissions. The functions makes use of the Flask-Login
extension for authentication and validation purposes.
"""
from flask_login import current_user, login_required

from ..repository.sql_alchemy_repository import SqlAlchemyRepository
from ..model.assignment import Assignment
from ..service.validator_helper import (
    validate_user,
    validate_space,
    validate_assignment,
    validate_admin,
    validate_no_assignment
)
from ..exception.service_exception import ServiceException

repository = SqlAlchemyRepository()


@login_required
def get_users_assignments():
    """
    Fetch assignments belonging to the current user.
    Returns:
        List[Assignment]: User's assignment objects.
    """
    return repository.get_all_by_filter(Assignment, Assignment.user_id == current_user.get_id())


@login_required
def get_assignments_by_space_id(space_id):
    """
    Retrieve assignments for a specific space, after user and space validation.
    Args:
        space_id (int): ID of the target space.
    Returns:
        List[Assignment]: Assignments within the specified space.
    """
    user = validate_user(current_user.get_id())
    space = validate_space(space_id)
    validate_assignment(space, user)
    return repository.get_all_by_filter(
        Assignment,
        Assignment.space_id == space.id
    )


@login_required
def create_assignment(space_id, user_id):
    """
    Create a new assignment of a space-user pair after validations.
    Args:
        space_id (int): ID of the target space.
        user_id (int): ID of the user to be assigned.
    """
    space = validate_space(space_id)
    caller_assignment = validate_assignment(
        space,
        validate_user(current_user.get_id())
    )
    validate_admin(caller_assignment)
    validate_no_assignment(
        space,
        validate_user(user_id)
    )
    repository.add(Assignment(space_id, user_id))


@login_required
def delete_assignment_by_space_id_user_id(space_id, user_id):
    """
    Delete a space-user pair assignment after validations.
    Args:
        space_id (int): ID of the target space.
        user_id (int): ID of the user associated with the assignment.
    """
    space = validate_space(space_id)
    to_be_deleted_assignment = validate_assignment(
        space,
        validate_user(user_id)
    )
    caller_assignment = validate_assignment(
        space,
        validate_user(current_user.get_id())
    )
    if to_be_deleted_assignment == caller_assignment:
        if caller_assignment.is_admin:
            raise ServiceException('Can\'t leave space when you\'re an admin')
    else:
        validate_admin(caller_assignment)
    repository.delete_by_id(Assignment, to_be_deleted_assignment.id)


@ login_required
def change_admin_permission(space_id, user_id, is_admin):
    """
    Modify admin permission for a user within a space after validations.
    Args:
        space_id (int): ID of the target space.
        user_id (int): ID of the user whose admin permission will be changed.
        is_admin (bool): New admin permission status for the user.
    """
    space = validate_space(space_id)
    caller_assignment = validate_assignment(
        space,
        validate_user(current_user.get_id())
    )
    validate_admin(caller_assignment)
    assignment = validate_assignment(
        space,
        validate_user(user_id)
    )
    if not isinstance(is_admin, bool):
        raise ServiceException('"is admin" must be type boolean')

    assignment.is_admin = is_admin
    repository.add(assignment)


def create_assignment_with_admin(space_id):
    """
    Create a new Assignment with admin privileges for the logged-in user.
    Args:
        space_id (int): ID of the target space.
    """
    assignment = Assignment(space_id, current_user.get_id())
    assignment.is_admin = True
    repository.add(assignment)


def delete_assignment(assignment):
    """
    Delete the provided assignment.
    Args:
        assignment (Assignment): The assignment to be deleted.
    """
    repository.delete_by_id(Assignment, assignment.id)
