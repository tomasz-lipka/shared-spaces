from flask import Blueprint, request, make_response
from exception.service_exception import ServiceException
import service.assignment_service as service
import json

assignment_controller = Blueprint('assignment_controller', __name__)


@assignment_controller.route('/spaces')
def get_spaces():
    """
    Endpoint
    Gets all Spaces. Shows where logged in user has admin role
    Logged in user must be member
    Returns: JSON
    """
    assignments = service.get_all()
    json_serializable_list = [assignment.to_dict() for assignment in assignments]
    return json.dumps(json_serializable_list)


@assignment_controller.route('/spaces/<int:space_id>/members')
def get_members(space_id):
    """
    Endpoint
    Gets members of a Space. Shows who has admin role
    Logged in user must be member
    Returns: JSON
    """
    try:
        assignments = service.get_all_by_space_id(space_id)
        json_serializable_list = [assignment.to_dict() for assignment in assignments]
        return json.dumps(json_serializable_list)
    except ServiceException as exc:
        return make_response(str(exc), 400)
