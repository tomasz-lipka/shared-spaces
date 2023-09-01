"""
This module defines an endpoint to retrieve image URLs associated
with a specific space ID
"""
import json
from flask import Blueprint, make_response
from injector import inject

from ..exception.service_exception import ServiceException
from ..media.image_service import ImageService

image_controller = Blueprint('image_controller', __name__)


@inject
@image_controller.route('/spaces/<int:space_id>/images')
def get_images(space_id, image_service: ImageService):
    """
    Get all image URLs within a space.
    Args:
        space_id (int): ID of the target space.
        image_service (ImageService): Instance of ImageService.
    Returns:
        str: JSON-encoded list of image URLs.
    """
    try:
        images = image_service.get_all_images(space_id)
        json_serializable_list = [{"media_url": image} for image in images]
        return json.dumps(json_serializable_list)
    except ServiceException as exc:
        return make_response(str(exc), 400)
