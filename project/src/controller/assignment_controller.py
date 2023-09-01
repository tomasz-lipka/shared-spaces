"""
Module containing the assignment controller blueprint with REST endpoints 
for managing space members, admin permissions and returns lists of spaces.
"""
import json
from flask import Blueprint, request, make_response
from injector import inject

from ..exception.service.service_exception import ServiceException
from ..service.entity.assignment_service import AssignmentService


assignment_controller = Blueprint('assignment_controller', __name__)


@inject
@assignment_controller.route('/spaces')
def get_spaces(service: AssignmentService):
    """
    Get a list of spaces for the logged-in user.
    Args:
        service (AssignmentService): Instance of AssignmentService.
    Returns:
        str: JSON representation of the list of spaces.
    """
    assignments = service.get_users_assignments()
    json_serializable_list = [assignment.spaces_to_dict()
                              for assignment in assignments]
    return json.dumps(json_serializable_list)


@inject
@assignment_controller.route('/spaces/<int:space_id>/members')
def get_members(space_id, service: AssignmentService):
    """
    Get a list of members in a space.
    Args:
        space_id (int): ID of the target space.
        service (AssignmentService): Instance of AssignmentService.
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


@inject
@assignment_controller.route('/spaces/<int:space_id>/members', methods=["POST"])
def post_member(space_id, service: AssignmentService):
    """
    Add a member to a space. Accept JSON payload with 'user-id'.
    Args:
        space_id (int): ID of the target space.
        service (AssignmentService): Instance of AssignmentService.
    Returns:
        str: Response message.
    """
    try:
        service.create_assignment(space_id, request.json['user-id'])
        return make_response('Member added', 200)
    except ServiceException as exc:
        return make_response(str(exc), 400)
    except KeyError as key_err:
        return make_response('Invalid payload: ' + str(key_err), 400)


@inject
@assignment_controller.route('/spaces/<int:space_id>/members/<int:user_id>', methods=["DELETE"])
def delete_member(space_id, user_id, service: AssignmentService):
    """
    Delete a member from a space.
    Args:
        space_id (int): ID of the target space.
        user_id (int): ID of the user to be removed from the space.
        service (AssignmentService): Instance of AssignmentService.
    Returns:
        str: Response message.
    """
    try:
        service.delete_assignment_by_space_id_user_id(space_id, user_id)
        return make_response('Member deleted', 200)
    except ServiceException as exc:
        return make_response(str(exc), 400)


@inject
@assignment_controller.route('/spaces/<int:space_id>/members/<int:user_id>', methods=["PUT"])
def put_admin(space_id, user_id, service: AssignmentService):
    """
    Change the admin permission for a member in a space.
    Accept JSON payload with 'is-admin'.
    Args:
        space_id (int): ID of the target space.
        user_id (int): ID of the user for whom the admin permission needs to be changed.
        service (AssignmentService): Instance of AssignmentService.
    Returns:
        str: Response message.
    """
    try:
        service.change_admin_permission(
            space_id, user_id, request.json['is-admin'])
        return make_response('Admin permission changed', 200)
    except ServiceException as exc:
        return make_response(str(exc), 400)
    except KeyError as key_err:
        return make_response('Invalid payload: ' + str(key_err), 400)
