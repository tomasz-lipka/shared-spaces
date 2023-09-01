"""
Module containing the ShareService class.
"""

from flask_login import current_user, login_required
from injector import inject

from ...repository.repository import Repository
from ..image.image_service import ImageService
from ...model.share import Share
from ..helper.service_validator import ServiceValidator
from ..helper.input_validator import validate_usr_input


class ShareService():
    """
    This class provides methods for creating, retrieving, editing, and deleting shares 
    within spaces. The methods are designed to work with Flask-Login for authentication. 
    It utilizes validation methods and makes use of ImageService to work with images.
    """

    MAX_TEXT_LEN = 200

    @inject
    def __init__(self, repository: Repository,
                 image_service: ImageService,  validator: ServiceValidator):
        self.repository = repository
        self.image_service = image_service
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
        validate_usr_input(text, 'Text', self.MAX_TEXT_LEN)
        self.validator.validate_assignment(
            self.validator.validate_space(space_id),
            self.validator.validate_user(current_user.get_id())
        )
        return self.repository.add(Share(space_id, current_user.get_id(), text))

    @login_required
    def get_share_by_share_id(self, share_id):
        """
        Retrieve a share by its share ID, validate ownership, and get the associated image URL.
        Args:
            share_id (int): The ID of the share to retrieve.
        Returns:
            Share: A Share object representing the retrieved share with the image URL included.
        """
        share = self.validator.validate_share(share_id)
        self.validator.validate_share_owner(share, int(current_user.get_id()))
        share.image_url = self.image_service.get_image(share)
        return share

    @login_required
    def get_shares_by_space_id(self, space_id):
        """
        Retrieve shares associated with a specific space based on its ID, validate user access
        and retrieve the image URL associated with each share.
        Args:
            space_id (int): The ID of the space for which shares should be retrieved.
        Returns:
            list of Share: A list of Share objects representing the shares associated with the
            specified space, each with the image URL included.
        """
        self.validator.validate_assignment(
            self.validator.validate_space(space_id),
            self.validator.validate_user(current_user.get_id())
        )
        shares = self.repository.get_all_by_filter(
            Share, Share.space_id == space_id)
        for share in shares:
            share.image_url = self.image_service.get_image(share)
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
        validate_usr_input(text, 'Text', self.MAX_TEXT_LEN)
        share = self.validator.validate_share(share_id)
        self.validator.validate_share_owner(
            share,
            int(current_user.get_id())
        )
        share.text = text
        return self.repository.add(share)
