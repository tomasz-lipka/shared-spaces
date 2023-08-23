"""
Module for managing spaces.

This module provides functions for creating, retrieving, renaming, and deleting spaces.
The functions are designed to work with Flask-Login for authentication and utilize validation 
functions from the validator_helper module. 
Additionally, the assignment_service module is used to perform assignment-related actions.
"""
from flask_login import current_user, login_required
from injector import inject

from ..repository.repository import Repository
from ..media.media_service import MediaService
from ..service.assignment_service import AssignmentService
from ..model.space import Space
from ..service.validator_helper import (
    validate_user,
    validate_space,
    validate_assignment,
    validate_admin,
    contains_only_owner
)


class SpaceService():

    @inject
    def __init__(self, repository: Repository, media_service: MediaService, assignment_service: AssignmentService):
        self.repository = repository
        self.media_service = media_service
        self.assignment_service = assignment_service

    @login_required
    def create_space(self, name):
        """
        Create a new space and assign the current user as the admin.
        Args:
            name (str): Name of the new space.
        """
        space_id = self.repository.add(Space(name))
        self.assignment_service.create_assignment_with_admin(space_id)

    @login_required
    def get_space_by_space_id(self, space_id):
        """
        Retrieve a space by its ID after validations.
        Args:
            space_id (int): ID of the target space.
        Returns:
            Space: The space object.
        """
        space = validate_space(space_id)
        validate_assignment(
            space,
            validate_user(current_user.get_id())
        )
        return space

    @login_required
    def delete_space_by_space_id(self, space_id):
        """
        Delete a space by its ID after validations and admin check.
        Args:
            space_id (int): ID of the target space.
        """
        space = validate_space(space_id)
        assignment = validate_assignment(
            space,
            validate_user(current_user.get_id())
        )
        validate_admin(assignment)
        if contains_only_owner(space):
            self.assignment_service.delete_assignment(assignment)
            self.repository.delete_by_id(Space, space_id)
            self.media_service.delete_space_directory(space)

    @login_required
    def rename_space(self, space_id, new_name):
        """
        Rename a space by its ID after validations and admin check.
        Args:
            space_id (int): ID of the target space.
            new_name (str): New name for the space.
        """
        space = validate_space(space_id)
        assignment = validate_assignment(
            space,
            validate_user(current_user.get_id())
        )
        validate_admin(assignment)

        space.name = new_name
        self.repository.add(space)
