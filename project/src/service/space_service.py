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
def get(space_id):
    """"""
    pass


@login_required
def create(name):
    """Creates a new space and assigns the user who creates it as admin"""
    space_id = repository.add(Space(name))
    member_service.create(current_user.get_id(), space_id)

@login_required
def delete(space_id):
    """"""
    pass

@login_required
def rename(space_id):
    """"""
    pass
