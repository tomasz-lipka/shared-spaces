from flask_login import current_user, login_required

from repository.sql_alchemy_repository import SqlAlchemyRepository
from exception.service_exception import ServiceException
from model.space import Space
import service.member_service as member_service


repository = SqlAlchemyRepository()


@login_required
def get_all_of_user():
    """Returns all spaces of user and shows where he's admin"""
    return member_service.get_all_by_user_id(current_user.get_id())


@login_required
def get_by_id(space_id):
    """
    Returns space by ID if user is member of requested space.
    Shows if the user is admin of it
    """
    space = member_service.get_by_id(current_user.get_id(), space_id)
    if not space:
        raise ServiceException('No such space or user not member of it')
    return space


@login_required
def create(name):
    """Creates a new space and assigns the user who creates it as admin"""
    space_id = repository.add(Space(name))
    member_service.create(current_user.get_id(), space_id)


@login_required
def get_members_by_space_id(space_id):
    """
    Returns a list of space members.
    Shows which users have admin priviliges.
    Only user who is member of the requested space can see it
    """
    space = get_by_id(space_id)
    return member_service.get_members_of_space(space.id)


@login_required
def delete(space_id):
    """Deletes and empty space if the logged in user is admin of it"""

    repository.delete_by_id(Space, space_id)


@login_required
def rename(space_id):
    """"""
    pass
