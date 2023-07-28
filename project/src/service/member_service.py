from repository.sql_alchemy_repository import SqlAlchemyRepository
from flask_login import login_required
from model.member import Member


repository = SqlAlchemyRepository()


@login_required
def create(user_id, space_id):
    """Creates a new member entity and grants admin role"""
    member = Member(user_id, space_id)
    member.is_admin = True
    repository.add(member)


@login_required
def get_all_by_user_id(user_id):
    """Returns all entities queried by user id"""
    return repository.get_all_by_filter(Member, Member.user_id == user_id)


@login_required
def get_by_id(user_id, space_id):
    """Returns space by space_id where user is member of"""
    spaces = repository.get_all_by_filter(Member, Member.user_id == user_id)
    for space in spaces:
        if space.id == space_id:
            return space
