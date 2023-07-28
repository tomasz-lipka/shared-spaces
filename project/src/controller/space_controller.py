from flask import Blueprint, request, make_response
from exception.service_exception import ServiceException
import service.space_service as service
import json

space_controller = Blueprint('space_controller', __name__)


@space_controller.route('/spaces')
def get_all_of_user():
    """
    Endpoint to get all spaces of the logfed in user 
    in which he is a member and show where he is admin.
    Returns a json format
    """
    spaces = service.get_all_of_user()
    json_serializable_list = [space.to_dict() for space in spaces]
    return json.dumps(json_serializable_list)


@space_controller.route('/spaces/<int:space_id>')
def get_by_id(space_id):
    """Endpoint to get a particular space of which the logged in user is member of"""
    try:
        space = service.get_by_id(space_id)
        return json.dumps(space.to_dict())
    except ServiceException as exc:
        return make_response(str(exc), 400)


@space_controller.route('/spaces', methods=["POST"])
def create():
    """Endpoint for creating a new space and getting admin of it"""
    try:
        data = request.json
        service.create(data['name'])
        return make_response('Space created', 200)
    except KeyError as key_err:
        return make_response('Invalid payload :' + str(key_err), 400)


@space_controller.route('/spaces/<int:space_id>/members')
def get_members_of_space(space_id):
    """
    Endpoint for getting a list of a spaces members.
    Works only if the logged in user is member of the requested space
    Shows which of the members are admins
    """
    try:
        members = service.get_members_by_space_id(space_id)
        json_serializable_list = [member.to_dict() for member in members]
        return json.dumps(json_serializable_list)
    except ServiceException as exc:
        return make_response(str(exc), 400)


@space_controller.route('/spaces/<int:space_id>', methods=["DELETE"])
def delete(space_id):
    """Endpoint for deleting an empty space of which the logged in user is admin"""
    try:
        service.delete(space_id)
        return make_response('Space deleted', 200)
    except ServiceException as exc:
        return make_response(str(exc), 400)


@space_controller.route('/spaces/<int:space_id>', methods=["PUT"])
def rename(space_id):
    """Endpoint for renaming a space of which the logged in user is admin"""
    pass
