from flask_login import current_user, login_required

from repository.sql_alchemy_repository import SqlAlchemyRepository
from exception.service_exception import ServiceException
from model.space import Space
import service.assignment_service as assignment_service


repository = SqlAlchemyRepository()


@login_required
def create(name):
    """
    Creates a new Space. Grants admin role to logged in user
    Returns: nothing
    """
    space_id = repository.add(Space(name))
    assignment_service.create(current_user.get_id(), space_id)


@login_required
def get_space_by_space_id(space_id):
    """
    Gets Space by space_id
    Logged in user must be member
    Returns: Space object
    """
    if not assignment_service.is_member(current_user.get_id(), space_id):
        raise ServiceException('User not member of space or no such space')
    return repository.get_by_id(Space, space_id)


# -------------------------------------------------------------------------------

# @login_required
# def delete_by_space_id(space_id):
#     """Deletes and empty space if the logged in user is member and admin of it"""
#     # space = get_by_space_id(space_id)
#     if not assignment_service.is_admin_by_space_id(current_user.get_id(), space_id):
#         raise ServiceException('Can\'t delete - not admin')
#     if not assignment_service.is_empty_by_space_id(current_user.get_id(), space_id):
#         raise ServiceException('Can\'t delete - not empty')
#     assignment_service.delete_by_space_id(current_user.get_id(), space.id)
#     repository.delete_by_id(Space, space.id)


@login_required
def rename(space_id):
    """"""
    pass
