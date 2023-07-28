from flask import Blueprint, request, make_response
from exception.service_exception import ServiceException
import service.space_service as service
import json

space_controller = Blueprint('space_controller', __name__)


@space_controller.route('/spaces', methods=["GET"])
def get_all_of_user():
    """
    Endpoint to get all spaces of the logfed in user 
    in which he is a member and show where he is admin.
    Returns a json format
    """
    spaces = service.get_all_of_user()
    json_serializable_list = [space.to_dict() for space in spaces]
    return json.dumps(json_serializable_list)


@space_controller.route('/spaces/<int:space_id>', methods=["GET"])
def get(space_id):
    """Endpoint to get a particular space of which the logged in user is member of"""
    pass


@space_controller.route('/spaces', methods=["POST"])
def create():
    """Endpoint for creating a new space and getting admin of it"""
    try:
        data = request.json
        service.create(data['name'])
        return make_response('Space created', 200)
    except KeyError as key_err:
        return make_response('Invalid payload :' + str(key_err), 400)


@space_controller.route('/spaces/<int:space_id>', methods=["DELETE"])
def delete(space_id):
    """Endpoint for deleting an empty space of which the logged in user is admin"""
    pass


@space_controller.route('/spaces/<int:space_id>', methods=["PUT"])
def rename(space_id):
    """Endpoint for renaming a space of which the logged in user is admin"""
    pass
