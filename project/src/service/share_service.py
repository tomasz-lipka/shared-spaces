from flask_login import current_user, login_required

from ..repository.sql_alchemy_repository import SqlAlchemyRepository
from ..model.share import Share
from ..service.validator_helper import validate_user, validate_space, validate_assignment, validate_admin, validate_no_assignment, validate_share, validate_share_owner
from ..exception.service_exception import ServiceException

repository = SqlAlchemyRepository()


@login_required
def create_share(space_id, text):
    validate_assignment(
        validate_user(current_user.get_id()),
        validate_space(space_id)
    )

    repository.add(Share(space_id, current_user.get_id(), text))


@login_required
def get_share_by_share_id(share_id):
    share = validate_share(share_id)
    validate_share_owner(share, int(current_user.get_id()))
    return share


@login_required
def get_shares_by_space_id(space_id):
    validate_assignment(
        validate_user(current_user.get_id()),
        validate_space(space_id)
    )
    return repository.get_all_by_filter(Share, Share.space_id == space_id)


@login_required
def delete_share_by_share_id(share_id):
    share = validate_share(share_id)
    validate_share_owner(share, int(current_user.get_id()))
    repository.delete_by_id(Share, share.id)


@login_required
def edit_share(share_id, text):
    share = validate_share(share_id)
    validate_share_owner(share, int(current_user.get_id()))
    share.text = text

    repository.add(share)
