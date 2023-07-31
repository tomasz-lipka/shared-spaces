from flask import Blueprint, request, make_response
from exception.service_exception import ServiceException
import service.space_service as service
import json

space_controller = Blueprint('space_controller', __name__)


@space_controller.route('/spaces', methods=["POST"])
def post_space():
    """
    Endpoint
    Invokes a service method: creates a space
    Returns: nothing
    """
    try:
        data = request.json
        service.create_space(data['name'])
        return make_response('Space created', 200)
    except KeyError as key_err:
        return make_response('Invalid payload :' + str(key_err), 400)

@space_controller.route('/spaces/<int:space_id>')
def get_space(space_id):
    """
    Endpoint
    Invokes a service method
    Returns: JSON (space object)
    """
    try:
        space = service.get_space_by_space_id(space_id)
        return json.dumps(space.to_dict())
    except ServiceException as exc:
        return make_response(str(exc), 400)


@space_controller.route('/spaces/<int:space_id>', methods=["DELETE"])
def delete_space(space_id):
    """
    Endpoint
    Invokes a service method: deletes a space
    Returns: nothing
    """
    try:
        service.delete_space_by_space_id(space_id)
        return make_response('Space deleted', 200)
    except ServiceException as exc:
        return make_response(str(exc), 400)


@space_controller.route('/spaces/<int:space_id>', methods=["PUT"])
def rename(space_id):
    """
    Endpoint 
    Invokes a service method: renames a space
    Returns: nothing
    """
    try:
        data = request.json
        service.rename_space(space_id, data['new-name'])
        return make_response('Space renamed', 200)
    except ServiceException as exc:
        return make_response(str(exc), 400)
    except KeyError as key_err:
        return make_response('Invalid payload :' + str(key_err), 400)
