"""
Module containing the share controller blueprint with REST endpoints
for managing shares within spaces.
"""
import json
from flask import Blueprint, request, make_response
from injector import inject

from ..exception.service_exception import ServiceException
from ..service.image.image_service import ImageService
from ..service.entity.share_service import ShareService

share_controller = Blueprint('share_controller', __name__)


@inject
@share_controller.route('/spaces/<int:space_id>/shares', methods=["POST"])
def post_share(space_id, image_service: ImageService, service: ShareService):
    """
    Create a new share in a space and optionally upload an image.
    Args:
        space_id (int): ID of the target space.
        image_service (ImageService): Instance of ImageService.
        service (ShareService): Instance of ShareService.
    Returns:
        str: Response message.
    """
    if not 'text' in request.form:
        return make_response("Text must be provided", 400)
    try:
        share_id = service.create_share(
            space_id,
            request.form['text']
        )
        if 'file' in request.files:
            image_service.upload_image(
                request.files['file'],
                share_id
            )
            return make_response('Share with image created', 200)
        return make_response('Share created', 200)
    except ServiceException as exc:
        return make_response(str(exc), 400)


@inject
@share_controller.route('/shares/<int:share_id>')
def get_share(share_id, service: ShareService):
    """
    Get details of a specific share by its share ID.
    Args:
        share_id (int): ID of the target share.
        service (ShareService): Instance of ShareService.
    Returns:
        str: JSON representation of the share details.
    """
    try:
        share = service.get_share_by_share_id(share_id)
        return json.dumps(share.to_dict())
    except ServiceException as exc:
        return make_response(str(exc), 400)


@inject
@share_controller.route('/spaces/<int:space_id>/shares')
def get_shares(space_id, service: ShareService):
    """
    Get a list of shares within a space.
    Args:
        space_id (int): ID of the target space.
        service (ShareService): Instance of ShareService.
    Returns:
        str: JSON representation of the list of shares.
    """
    try:
        shares = service.get_shares_by_space_id(space_id)
        json_serializable_list = [share.shares_to_dict() for share in shares]
        return json.dumps(json_serializable_list)
    except ServiceException as exc:
        return make_response(str(exc), 400)


@inject
@share_controller.route('/shares/<int:share_id>', methods=["DELETE"])
def delete_share(share_id, service: ShareService):
    """
    Delete a share by its share ID.
    Args:
        share_id (int): ID of the target share.
        service (ShareService): Instance of ShareService.
    Returns:
        str: Response message.
    """
    try:
        service.delete_share_by_share_id(share_id)
        return make_response('Share deleted', 200)
    except ServiceException as exc:
        return make_response(str(exc), 400)


@inject
@share_controller.route('/shares/<int:share_id>', methods=["PUT"])
def put_share(share_id, service: ShareService, image_service: ImageService):
    """
    Update a share's text and optionally upload an new image.
    Args:
        share_id (int): ID of the target share.
        service (ShareService): Instance of ShareService.
        image_service (ImageService): Instance of ImageService.
    Returns:
        str: Response message.
    """
    if not 'text' in request.form:
        return make_response("Text must be provided", 400)
    try:
        share_id = service.edit_share(
            share_id,
            request.form['text']
        )
        if 'file' in request.files:
            image_service.upload_image(
                request.files['file'],
                share_id
            )
        return make_response('Share edited', 200)
    except ServiceException as exc:
        return make_response(str(exc), 400)
