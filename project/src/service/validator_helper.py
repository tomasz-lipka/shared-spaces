"""
Module containing helper functions for validating users, spaces, assignments, and shares.

This module provides functions for validating user identities, space assignments, admin privileges,
and ownership of shares. It interacts with the repository for database queries and raises
ServiceException for various validation failures.
"""
from ..repository.sql_alchemy_repository import SqlAlchemyRepository
from ..model.user import User
from ..model.space import Space
from ..model.assignment import Assignment
from ..model.share import Share
from ..exception.service_exception import ServiceException

repository = SqlAlchemyRepository()


def validate_space(space_id):
    """
    Validate if space exists and retrieve a space by its ID.
    Args:
        space_id (int): ID of the target space.
    Returns:
        Space: The validated space object.
    """
    space = repository.get_by_id(Space, space_id)
    if not space:
        raise ServiceException(f"Space with ID '{space_id}' doesn't exist")
    return space


def validate_user(user_id):
    """
    Validate if user exists and retrieve a user by their ID.
    Args:
        user_id (int): ID of the target user.
    Returns:
        User: The validated user object.
    """
    user = repository.get_by_id(User, user_id)
    if not user:
        raise ServiceException(f"User with ID '{user_id}' doesn't exist")
    return user


def validate_assignment(space, user):
    """
    Validate if space-user (assignment) pair exists and retrieve it.
    Args:
        space (Space): The space object for validation.
        user (User): The user object for validation.
    Returns:
        Assignment: The validated assignment object.
    """
    assignment = repository.get_first_by_two_filters(
        Assignment, Assignment.user_id == user.id, Assignment.space_id == space.id)
    if not assignment:
        raise ServiceException('User-space pair doesn\'t exist')
    return assignment


def validate_no_assignment(space, user):
    """
    Validate that no assignment exists for a specific space-user pair.
    Args:
        space (Space): The space object for validation.
        user (User): The user object for validation.
    """
    if repository.get_first_by_two_filters(Assignment,
                                           Assignment.user_id == user.id,
                                           Assignment.space_id == space.id
                                           ):
        raise ServiceException('User-space pair already exists')


def validate_admin(assignment):
    """
    Validate that a user has admin privileges within a space.
    Args:
        assignment (Assignment): The assignment object for validation.
    """
    if not assignment.is_admin:
        raise ServiceException('User not admin')


def contains_only_owner(space):
    """
    Validate if there is only one space-user pair assignment.
    Args:
        space (Space): The space object for validation.
    Returns:
        bool: True if the space contains only one user, False otherwise.
    """
    assignments = repository.get_all_by_filter(
        Assignment, Assignment.space_id == space.id)
    if len(assignments) != 1:
        raise ServiceException('Space not empty')
    return True


def validate_share(share_id):
    """
    Validate if share exists and retrieve a share by its ID.
    Args:
        share_id (int): ID of the target share. 
    Returns:
        Share: The validated share object.
    """
    share = repository.get_by_id(Share, share_id)
    if not share:
        raise ServiceException('No such share')
    return share


def validate_share_owner(share, user_id):
    """
    Validate if a user owns a specific share.
    Args:
        share (Share): The share object for validation.
        user_id (int): ID of the user to be validated as the owner.
    """
    if not share.user_id == user_id:
        raise ServiceException('User doesn\'t own this share')
