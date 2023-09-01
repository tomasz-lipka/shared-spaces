"""
Module containing the SpaceService class.
"""

from flask_login import current_user, login_required
from injector import inject

from ...repository.repository import Repository
from ..image.image_service import ImageService
from .assignment_service import AssignmentService
from ...model.space import Space
from ..helper.validator_helper import ValidatorHelper
from ..helper.input_validator import validate_usr_input


class SpaceService():
    """
    This class provides methods for creating, retrieving, renaming, and deleting spaces.
    The methods are designed to work with Flask-Login for authentication. It utilizes validation
    methods and makes use of ImageService to work with images. 
    Additionally, the AssignmentService class is used to perform assignment-related actions.
    """

    MAX_NAME_LEN = 15

    @inject
    def __init__(self,
                 repository: Repository, image_service: ImageService,
                 assignment_service: AssignmentService, validator: ValidatorHelper):
        self.repository = repository
        self.image_service = image_service
        self.assignment_service = assignment_service
        self.validator = validator

    @login_required
    def create_space(self, name):
        """
        Create a new space and assign the current user as the admin.
        Args:
            name (str): Name of the new space.
        """
        self.validator.validate_not_null(name, 'Name')
        validate_usr_input(name, 'Name', self.MAX_NAME_LEN)
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
        space = self.validator.validate_space(space_id)
        self.validator.validate_assignment(
            space,
            self.validator.validate_user(current_user.get_id())
        )
        return space

    @login_required
    def delete_space_by_space_id(self, space_id):
        """
        Delete a space by its ID after validations and admin check.
        Args:
            space_id (int): ID of the target space.
        """
        space = self.validator.validate_space(space_id)
        assignment = self.validator.validate_assignment(
            space,
            self.validator.validate_user(current_user.get_id())
        )
        self.validator.validate_admin(assignment)
        if self.validator.contains_only_owner(space):
            self.assignment_service.delete_assignment(assignment)
            self.repository.delete_by_id(Space, space_id)
            self.image_service.delete_space_directory(space)

    @login_required
    def rename_space(self, space_id, new_name):
        """
        Rename a space by its ID after validations and admin check.
        Args:
            space_id (int): ID of the target space.
            new_name (str): New name for the space.
        """
        self.validator.validate_not_null(new_name, 'New name')
        validate_usr_input(new_name, 'Name', self.MAX_NAME_LEN)
        space = self.validator.validate_space(space_id)
        assignment = self.validator.validate_assignment(
            space,
            self.validator.validate_user(current_user.get_id())
        )
        self.validator.validate_admin(assignment)

        space.name = new_name
        self.repository.add(space)
