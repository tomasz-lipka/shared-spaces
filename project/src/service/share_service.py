"""
Module for managing shares within spaces.

This module provides functions for creating, retrieving, editing, and deleting shares within spaces.
The functions are designed to work with Flask-Login for authentication and utilize validation
functions from the validator_helper module.
"""
from flask_login import current_user, login_required

from ..repository.sql_alchemy_repository import SqlAlchemyRepository
from ..model.share import Share
from ..media.aws_service import AwsService
from ..service.validator_helper import (
    validate_user,
    validate_space,
    validate_assignment,
    validate_share,
    validate_share_owner
)

repository = SqlAlchemyRepository()
media_service = AwsService()


@login_required
def create_share(space_id, text):
    """
    Create a new share within a space after validations.
    Args:
        space_id (int): ID of the target space.
        text (str): Text content of the share.
    Returns:
        int: The ID of the newly created share.
    """
    validate_assignment(
        validate_space(space_id),
        validate_user(current_user.get_id())
    )
    return repository.add(Share(space_id, current_user.get_id(), text))


@login_required
def get_share_by_share_id(share_id):
    share = validate_share(share_id)
    validate_share_owner(share, int(current_user.get_id()))
    share.media_url = media_service.get_image(share)
    return share


@login_required
def get_shares_by_space_id(space_id):
    validate_assignment(
        validate_space(space_id),
        validate_user(current_user.get_id())
    )
    shares = repository.get_all_by_filter(Share, Share.space_id == space_id)
    for share in shares:
        share.media_url = media_service.get_image(share)
    return shares


@login_required
def delete_share_by_share_id(share_id):
    """
    Delete a share by its ID after owner validation.
    Args:
        share_id (int): ID of the target share.
    """
    share = validate_share(share_id)
    validate_share_owner(
        share,
        int(current_user.get_id())
    )
    repository.delete_by_id(Share, share.id)


@login_required
def edit_share(share_id, text):
    """
    Edit the text of a share by its ID after owner validation.
    Args:
        share_id (int): ID of the target share.
        text (str): Updated text content of the share.
    """
    share = validate_share(share_id)
    validate_share_owner(
        share,
        int(current_user.get_id())
    )
    share.text = text
    repository.add(share)
