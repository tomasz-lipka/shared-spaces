from flask import Blueprint, request, make_response
from exception.service_exception import ServiceException
import service.assignment_service as service
import json


assignment_controller = Blueprint('assignment_controller', __name__)


@assignment_controller.route('/spaces')
def get_spaces():
    """
    Endpoint
    Gets all Spaces of logged in user. Shows where he's admin
    Returns: JSON
    """
    assignments = service.get_users_assignments()
    json_serializable_list = [assignment.to_dict() for assignment in assignments]
    return json.dumps(json_serializable_list)


@assignment_controller.route('/spaces/<int:space_id>/members')
def get_members(space_id):
    """
    Endpoint
    Gets members of a Space. Shows who has admin role
    Logged in user must be: member
    Returns: JSON
    """
    try:
        assignments = service.get_assignments_by_space_id(space_id)
        json_serializable_list = [assignment.to_dict() for assignment in assignments]
        return json.dumps(json_serializable_list)
    except ServiceException as exc:
        return make_response(str(exc), 400)

@assignment_controller.route('/spaces/<int:space_id>/members', methods=["POST"])
def post_member(space_id):
    """
    Endpoint
    Adds a new member. Member musn't be in the space
    Logged in user must be: member, admin
    Returns: nothing
    """
    try:
        data = request.json
        service.create_assignment(data['user-id'], space_id)
        return make_response('Member added', 200)
    except ServiceException as exc:
        return make_response(str(exc), 400)
    except KeyError as key_err:
        return make_response('Invalid payload :' + str(key_err), 400)


@assignment_controller.route('/spaces/<int:space_id>/members/<int:user_id>', methods=["DELETE"])
def delete_member(space_id, user_id):
    try:
        service.delete_assignment_by_user_id_space_id(space_id, user_id)
        return make_response('Member deleted', 200)
    except ServiceException as exc:
        return make_response(str(exc), 400)


@assignment_controller.route('/spaces/<int:space_id>/members/<int:user_id>', methods=["PUT"])
def put_admin(space_id, user_id):
    try:
        data = request.json
        service.change_admin_permission(space_id, user_id, data['is-admin'])
        return make_response('Admin permission changed', 200)
    except ServiceException as exc:
        return make_response(str(exc), 400)
    except KeyError as key_err:
        return make_response('Invalid payload :' + str(key_err), 400)