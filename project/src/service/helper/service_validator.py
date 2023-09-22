"""
Module containing the ServiceValidator class.
"""
from injector import inject
from flask_jwt_extended import get_jwt_identity

from ...exception.service.service_exception import ServiceException
from ...exception.service.not_found_exception import NotFoundException
from ...exception.service.forbidden_exception import ForbiddenException
from ...repository.repository import Repository
from ...model.user import User
from ...model.space import Space
from ...model.assignment import Assignment
from ...model.share import Share


class ServiceValidator():
    """
    This class provides methods for validating user identities, space assignments, admin privileges,
    and ownership of shares. It interacts with the repository for database queries and raises
    ServiceException for various validation failures.
    """

    @inject
    def __init__(self, repository: Repository):
        self.repository = repository

    def validate_space(self, space_id):
        """
        Validate if space exists and retrieve a space by its ID.
        Args:
            space_id (int): ID of the target space.
        Returns:
            Space: The validated space object.
        """
        space = self.repository.get_by_id(Space, space_id)
        if not space:
            raise NotFoundException(
                f"Space with ID '{space_id}' doesn't exist")
        return space

    def validate_user(self, user_id):
        """
        Validate if user exists and retrieve a user by their ID.
        Args:
            user_id (int): ID of the target user.
        Returns:
            User: The validated user object.
        """
        user = self.repository.get_by_id(User, user_id)
        if not user:
            raise NotFoundException(
                f"User with ID '{user_id}' doesn't exist")
        return user

    def get_logged_in_user_id(self):
        """
        Retrieves user_id of the logged-in user based on the JWT identity.
        Returns:
            int: The user id.
        """
        user = self.repository.get_first_by_filter(
            User, User.login == get_jwt_identity())
        return user.id

    def validate_assignment(self, space, user):
        """
        Validate if space-user (assignment) pair exists and retrieve it.
        Args:
            space (Space): The space object for validation.
            user (User): The user object for validation.
        Returns:
            Assignment: The validated assignment object.
        """
        assignment = self.repository.get_first_by_two_filters(
            Assignment, Assignment.user_id == user.id, Assignment.space_id == space.id)
        if not assignment:
            raise ForbiddenException('User-space pair doesn\'t exist')
        return assignment

    def validate_no_assignment(self, space, user):
        """
        Validate that no assignment exists for a specific space-user pair.
        Args:
            space (Space): The space object for validation.
            user (User): The user object for validation.
        """
        if self.repository.get_first_by_two_filters(Assignment,
                                                    Assignment.user_id == user.id,
                                                    Assignment.space_id == space.id
                                                    ):
            raise ServiceException('User-space pair already exists', 400)

    def validate_admin(self, assignment):
        """
        Validate that a user has admin privileges within a space.
        Args:
            assignment (Assignment): The assignment object for validation.
        """
        if not assignment.is_admin:
            raise ForbiddenException('User not admin')

    def contains_only_owner(self, space):
        """
        Validate if there is only one space-user pair assignment.
        Args:
            space (Space): The space object for validation.
        Returns:
            bool: True if the space contains only one user, False otherwise.
        """
        assignments = self.repository.get_all_by_filter(
            Assignment, Assignment.space_id == space.id)
        if len(assignments) != 1:
            raise ServiceException('Space not empty', 400)
        return True

    def validate_share(self, share_id):
        """
        Validate if share exists and retrieve a share by its ID.
        Args:
            share_id (int): ID of the target share. 
        Returns:
            Share: The validated share object.
        """
        share = self.repository.get_by_id(Share, share_id)
        if not share:
            raise NotFoundException('No such share')
        return share

    def validate_share_owner(self, share, user_id):
        """
        Validate if a user owns a specific share.
        Args:
            share (Share): The share object for validation.
            user_id (int): ID of the user to be validated as the owner.
        """
        if not share.user_id == user_id:
            raise ForbiddenException('User doesn\'t own this share')

    def validate_not_null(self, usr_input, input_name):
        """
        Validate that a user input is not `None`.
        Args:
            usr_input: The user input to be validated.
            input_name (str): The name of the input parameter (for error messages).
        """
        if usr_input is None:
            raise ServiceException(f"{input_name} must be provided", 400)

    def validate_last_admin(self, assignment, is_admin):
        """
        Validate if space has at least one admin before changing admin permissions.
        Args:
            assignment (Assignment): The assignment object for validation.
            is_admin: admin state.
        """
        if not is_admin:
            assignments = self.repository.get_all_by_two_filters(
                Assignment, bool(Assignment.is_admin), Assignment.space_id == assignment.space_id)
            if len(assignments) == 1:
                raise ServiceException(
                    'Space must have at least one admin', 400)
