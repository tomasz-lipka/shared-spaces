"""
Module containing the space controller blueprint with REST endpoints 
for managing spaces.
"""
import json
from flask import Blueprint, request, make_response
from injector import inject

from ..exception.service_exception import ServiceException
from ..service.entity.space_service import SpaceService

space_controller = Blueprint('space_controller', __name__)


@inject
@space_controller.route('/spaces', methods=["POST"])
def post_space(service: SpaceService):
    """
    Create a new space. Accepts a JSON payload with 'name'.
    Args:
        service (SpaceService): Instance of SpaceService.
    Returns:
        str: Response message.
    """
    try:
        service.create_space(request.json['name'])
        return make_response('Space created', 200)
    except KeyError as key_err:
        return make_response('Invalid payload: ' + str(key_err), 400)
    except ServiceException as exc:
        return make_response(str(exc), 400)


@inject
@space_controller.route('/spaces/<int:space_id>')
def get_space(space_id, service: SpaceService):
    """
    Get details of a space by its ID.
    Args:
        space_id (int): ID of the target space.
        service (SpaceService): Instance of SpaceService.
    Returns:
        str: JSON representation of the space details.
    """
    try:
        space = service.get_space_by_space_id(space_id)
        return json.dumps(space.to_dict())
    except ServiceException as exc:
        return make_response(str(exc), 400)


@inject
@space_controller.route('/spaces/<int:space_id>', methods=["DELETE"])
def delete_space(space_id, service: SpaceService):
    """
    Delete a space by its ID.
    Args:
        space_id (int): ID of the target space.
        service (SpaceService): Instance of SpaceService.
    Returns:
        str: Response message.
    """
    try:
        service.delete_space_by_space_id(space_id)
        return make_response('Space deleted', 200)
    except ServiceException as exc:
        return make_response(str(exc), 400)


@inject
@space_controller.route('/spaces/<int:space_id>', methods=["PUT"])
def rename(space_id, service: SpaceService):
    """
    Rename a space by its ID. Accepts a JSON payload with 'new-name'.
    Args:
        space_id (int): ID of the target space.
        service (SpaceService): Instance of SpaceService.
    Returns:
        str: Response message.
    """
    try:
        service.rename_space(space_id, request.json['new-name'])
        return make_response('Space renamed', 200)
    except ServiceException as exc:
        return make_response(str(exc), 400)
    except KeyError as key_err:
        return make_response('Invalid payload: ' + str(key_err), 400)
