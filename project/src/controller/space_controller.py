from flask import Blueprint, request, make_response
from exception.service_exception import ServiceException
import service.space_service as service
import json

space_controller = Blueprint('space_controller', __name__)


@space_controller.route('/spaces', methods=["POST"])
def post_space():
    """
    Endpoint
    Creates a new Space. Makes logged in user admin
    Returns: nothing
    """
    try:
        data = request.json
        service.create(data['name'])
        return make_response('Space created', 200)
    except KeyError as key_err:
        return make_response('Invalid payload :' + str(key_err), 400)


@space_controller.route('/spaces/<int:space_id>')
def get_space(space_id):
    """
    Endpoint
    Gets a Space by space_id
    Logged in user must be member
    Returns: JSON
    """
    try:
        space = service.get_space_by_space_id(space_id)
        return json.dumps(space.to_dict())
    except ServiceException as exc:
        return make_response(str(exc), 400)


# -------------------------------------------------------------------------------


# @space_controller.route('/spaces/<int:space_id>', methods=["DELETE"])
# def delete(space_id):
#     """Endpoint for deleting an empty space of which the logged in user is admin and member"""
#     try:
#         service.delete_by_space_id(space_id)
#         return make_response('Space deleted', 200)
#     except ServiceException as exc:
#         return make_response(str(exc), 400)


@space_controller.route('/spaces/<int:space_id>', methods=["PUT"])
def rename(space_id):
    """Endpoint for renaming a space of which the logged in user is admin"""
    pass
