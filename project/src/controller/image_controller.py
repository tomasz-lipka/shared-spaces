"""
This module defines an endpoint to retrieve image URLs associated
with a specific space ID
"""
import json
from flask import Blueprint, make_response
from injector import inject

from ..exception.service_exception import ServiceException
from ..media.aws_service import MediaService

image_controller = Blueprint('image_controller', __name__)


@inject
@image_controller.route('/spaces/<int:space_id>/images')
def get_images(space_id, media_service: MediaService):
    """
    Get all image URLs within a space.
    Args:
        space_id (int): ID of the target space.
        media_service (MediaService): Instance of MediaService.
    Returns:
        str: JSON-encoded list of image URLs.
    """
    try:
        images = media_service.get_all_media_urls(space_id)
        json_serializable_list = [{"media_url": image} for image in images]
        return json.dumps(json_serializable_list)
    except ServiceException as exc:
        return make_response(str(exc), 400)
