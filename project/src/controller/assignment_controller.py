"""
Module containing the assignment controller blueprint with REST endpoints 
for managing space members, admin permissions and returns lists of spaces.
"""
import json
from flask import Blueprint, request, make_response

from ..exception.service_exception import ServiceException
from ..service import assignment_service as service


assignment_controller = Blueprint('assignment_controller', __name__)


@assignment_controller.route('/spaces')
def get_spaces():
    """
    Get a list of spaces for the logged-in user.
    Returns:
        str: JSON representation of the list of spaces.
    """
    assignments = service.get_users_assignments()
    json_serializable_list = [assignment.spaces_to_dict()
                              for assignment in assignments]
    return json.dumps(json_serializable_list)


@assignment_controller.route('/spaces/<int:space_id>/members')
def get_members(space_id):
    """
    Get a list of members in a space.
    Args:
        space_id (int): ID of the target space.
    Returns:
        str: JSON representation of the list of members.
    """
    try:
        assignments = service.get_assignments_by_space_id(space_id)
        json_serializable_list = [assignment.users_to_dict()
                                  for assignment in assignments]
        return json.dumps(json_serializable_list)
    except ServiceException as exc:
        return make_response(str(exc), 400)


@assignment_controller.route('/spaces/<int:space_id>/members', methods=["POST"])
def post_member(space_id):
    """
    Add a member to a space. Accept JSON payload with 'user-id'.
    Args:
        space_id (int): ID of the target space.
    Returns:
        str: Response message.
    """
    try:
        data = request.json
        service.create_assignment(space_id, data['user-id'])
        return make_response('Member added', 200)
    except ServiceException as exc:
        return make_response(str(exc), 400)
    except KeyError as key_err:
        return make_response('Invalid payload: ' + str(key_err), 400)


@assignment_controller.route('/spaces/<int:space_id>/members/<int:user_id>', methods=["DELETE"])
def delete_member(space_id, user_id):
    """
    Delete a member from a space.
    Args:
        space_id (int): ID of the target space.
        user_id (int): ID of the user to be removed from the space.
    Returns:
        str: Response message.
    """
    try:
        service.delete_assignment_by_space_id_user_id(space_id, user_id)
        return make_response('Member deleted', 200)
    except ServiceException as exc:
        return make_response(str(exc), 400)


@assignment_controller.route('/spaces/<int:space_id>/members/<int:user_id>', methods=["PUT"])
def put_admin(space_id, user_id):
    """
    Change the admin permission for a member in a space.
    Accept JSON payload with 'is-admin'.
    Args:
        space_id (int): ID of the target space.
        user_id (int): ID of the user for whom the admin permission needs to be changed.
    Returns:
        str: Response message.
    """
    try:
        data = request.json
        service.change_admin_permission(space_id, user_id, data['is-admin'])
        return make_response('Admin permission changed', 200)
    except ServiceException as exc:
        return make_response(str(exc), 400)
    except KeyError as key_err:
        return make_response('Invalid payload: ' + str(key_err), 400)
