"""
Module containing the AssignmentService class.
"""
from flask_login import current_user, login_required
from injector import inject

from ...repository.repository import Repository
from ...model.assignment import Assignment
from ..helper.service_validator import ServiceValidator
from ...exception.service.service_exception import ServiceException


class AssignmentService():
    """
    This class provides methods for fetching, creating, modifying, and deleting user assignments
    and their associated permissions. The methods make use of the Flask-Login
    extension for authentication and utilizes validation methods.
    """
    @inject
    def __init__(self, repository: Repository,  validator: ServiceValidator):
        self.repository = repository
        self.validator = validator

    @login_required
    def get_users_assignments(self):
        """
        Fetch assignments belonging to the current user.
        Returns:
            List[Assignment]: User's assignment objects.
        """
        return self.repository.get_all_by_filter(Assignment, Assignment.user_id == current_user.get_id())

    @login_required
    def get_assignments_by_space_id(self, space_id):
        """
        Retrieve assignments for a specific space, after user and space validation.
        Args:
            space_id (int): ID of the target space.
        Returns:
            List[Assignment]: Assignments within the specified space.
        """
        user = self.validator.validate_user(current_user.get_id())
        space = self.validator.validate_space(space_id)
        self.validator.validate_assignment(space, user)
        return self.repository.get_all_by_filter(
            Assignment,
            Assignment.space_id == space.id
        )

    @login_required
    def create_assignment(self, space_id, user_id):
        """
        Create a new assignment of a space-user pair after validations.
        Args:
            space_id (int): ID of the target space.
            user_id (int): ID of the user to be assigned.
        """
        self.validator.validate_not_null(user_id, 'User id')
        space = self.validator.validate_space(space_id)
        caller_assignment = self.validator.validate_assignment(
            space,
            self.validator.validate_user(current_user.get_id())
        )
        self.validator.validate_admin(caller_assignment)
        self.validator.validate_no_assignment(
            space,
            self.validator.validate_user(user_id)
        )
        self.repository.add(Assignment(space_id, user_id))

    @login_required
    def delete_assignment_by_space_id_user_id(self, space_id, user_id):
        """
        Delete a space-user pair assignment after validations.
        Args:
            space_id (int): ID of the target space.
            user_id (int): ID of the user associated with the assignment.
        """
        space = self.validator.validate_space(space_id)
        to_be_deleted_assignment = self.validator.validate_assignment(
            space,
            self.validator.validate_user(user_id)
        )
        caller_assignment = self.validator.validate_assignment(
            space,
            self.validator.validate_user(current_user.get_id())
        )
        if to_be_deleted_assignment == caller_assignment:
            if caller_assignment.is_admin:
                raise ServiceException(
                    'Can\'t leave space when you\'re an admin')
        else:
            self.validator.validate_admin(caller_assignment)
        self.repository.delete_by_id(Assignment, to_be_deleted_assignment.id)

    @login_required
    def change_admin_permission(self, space_id, user_id, is_admin):
        """
        Modify admin permission for a user within a space after validations.
        Args:
            space_id (int): ID of the target space.
            user_id (int): ID of the user whose admin permission will be changed.
            is_admin (bool): New admin permission status for the user.
        """
        self.validator.validate_not_null(is_admin, 'Is admin')
        space = self.validator.validate_space(space_id)
        caller_assignment = self.validator.validate_assignment(
            space,
            self.validator.validate_user(current_user.get_id())
        )
        self.validator.validate_admin(caller_assignment)
        assignment = self.validator.validate_assignment(
            space,
            self.validator.validate_user(user_id)
        )
        if not isinstance(is_admin, bool):
            raise ServiceException('"is admin" must be type boolean')

        assignment.is_admin = is_admin
        self.repository.add(assignment)

    def create_assignment_with_admin(self, space_id):
        """
        Create a new Assignment with admin privileges for the logged-in user.
        Args:
            space_id (int): ID of the target space.
        """
        assignment = Assignment(space_id, current_user.get_id())
        assignment.is_admin = True
        self.repository.add(assignment)

    def delete_assignment(self, assignment):
        """
        Delete the provided assignment.
        Args:
            assignment (Assignment): The assignment to be deleted.
        """
        self.repository.delete_by_id(Assignment, assignment.id)
