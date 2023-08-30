"""
Module for managing shares within spaces.

This module provides functions for creating, retrieving, editing, and deleting shares within spaces.
The functions are designed to work with Flask-Login for authentication and utilize validation
functions from the validator_helper module.
"""
from flask_login import current_user, login_required
from injector import inject

from ..repository.repository import Repository
from ..media.media_service import MediaService
from ..model.share import Share
from ..service.validator_helper import ValidatorHelper
from ..service.input_validator import validate_usr_input


class ShareService():

    @inject
    def __init__(self, repository: Repository,
                 media_service: MediaService,  validator: ValidatorHelper):
        self.repository = repository
        self.media_service = media_service
        self.validator = validator

    @login_required
    def create_share(self, space_id, text):
        """
        Create a new share within a space after validations.
        Args:
            space_id (int): ID of the target space.
            text (str): Text content of the share.
        Returns:
            int: The ID of the newly created share.
        """
        validate_usr_input(text, 'Text', 200)
        self.validator.validate_assignment(
            self.validator.validate_space(space_id),
            self.validator.validate_user(current_user.get_id())
        )
        return self.repository.add(Share(space_id, current_user.get_id(), text))

    @login_required
    def get_share_by_share_id(self, share_id):
        share = self.validator.validate_share(share_id)
        self.validator.validate_share_owner(share, int(current_user.get_id()))
        share.media_url = self.media_service.get_image(share)
        return share

    @login_required
    def get_shares_by_space_id(self, space_id):
        self.validator.validate_assignment(
            self.validator.validate_space(space_id),
            self.validator.validate_user(current_user.get_id())
        )
        shares = self.repository.get_all_by_filter(
            Share, Share.space_id == space_id)
        for share in shares:
            share.media_url = self.media_service.get_image(share)
        return shares

    @login_required
    def delete_share_by_share_id(self, share_id):
        """
        Delete a share by its ID after owner validation.
        Args:
            share_id (int): ID of the target share.
        """
        share = self.validator.validate_share(share_id)
        self.validator.validate_share_owner(
            share,
            int(current_user.get_id())
        )
        self.repository.delete_by_id(Share, share.id)

    @login_required
    def edit_share(self, share_id, text):
        """
        Edit the text of a share by its ID after owner validation.
        Args:
            share_id (int): ID of the target share.
            text (str): Updated text content of the share.
        """
        share = self.validator.validate_share(share_id)
        self.validator.validate_share_owner(
            share,
            int(current_user.get_id())
        )
        share.text = text
        return self.repository.add(share)
