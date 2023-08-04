from flask_login import current_user, login_required

from ..repository.sql_alchemy_repository import SqlAlchemyRepository
from ..exception.service_exception import ServiceException
from ..model.space import Space
# import service.assignment_service as assignment_service
from  ..service import assignment_service as assignment_service
from ..service.validator_helper import *

repository = SqlAlchemyRepository()


@login_required
def create_space(name):
    """
    Adds a new Space to repo. Invokes a service method: creates assignment
    Returns: nothing
    """
    space_id = repository.add(Space(name))
    assignment_service.create_assignment_with_admin(space_id)


@login_required
def get_space_by_space_id(space_id):
    """
    Invokes validators: if space exists, if user exists, if space-user assignment exists 
    Returns: Space object
    """
    space = validate_space(space_id)
    validate_assignment(validate_user(current_user.get_id()), space)
    return space


@login_required
def delete_space_by_space_id(space_id):
    """
    Invokes validators: if space exists, if user exists, if space-user assignment exists, if is admin, if is empty
    Invokes a service method: deletes assignment
    Deletes space from repo
    Returns: nothing
    """
    space = validate_space(space_id)
    assignment = validate_assignment(validate_user(current_user.get_id()), space)
    validate_admin(assignment)
    if contains_only_owner(space):
        assignment_service.delete_assignment(assignment)
        repository.delete_by_id(Space, space_id)


@login_required
def rename_space(space_id, new_name):
    """
    Invokes validators: if space exists, if user exists, if space-user assignment exists, if is admin
    Renames a space in repo
    Returns: nothing
    """
    space = validate_space(space_id)
    assignment = validate_assignment(validate_user(current_user.get_id()), space)
    validate_admin(assignment)

    space.name = new_name
    repository.add(space)
