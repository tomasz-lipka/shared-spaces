"""
Module containing the user controller blueprint with REST endpoints 
for managing user related operations.
"""
from flask import Blueprint, request, make_response

from ..exception.service_exception import ServiceException
from ..service import user_service as service

user_controller = Blueprint('user_controller', __name__)


@user_controller.route('/login', methods=["POST"])
def login():
    """
    Log the user in.
    Accepts a JSON payload with 'login' and 'password'.
    Returns:
        str: Response message.
    """
    try:
        data = request.json
        service.login(data['login'], data['password'])
        return make_response('Logged in', 200)
    except ServiceException as exc:
        return make_response(str(exc), 401)
    except KeyError as key_err:
        return make_response('Invalid payload :' + str(key_err), 400)


@user_controller.route('/register', methods=["POST"])
def register():
    """
    Register a new user.
    Accepts a JSON payload with 'login', 'password', and 'confirm-password'.
    Returns:
        str: Response message.
    """
    try:
        data = request.json
        service.create_user(
            data['login'], data['password'], data['confirm-password'])
        return make_response('User created', 200)
    except ServiceException as exc:
        return make_response(str(exc), 400)
    except KeyError as key_err:
        return make_response('Invalid payload :' + str(key_err), 400)


@user_controller.route('/logout')
def logout():
    """
    Log the user out.
    Returns:
        str: Response message.
    """
    service.logout()
    return make_response('Logged out', 200)


@user_controller.route('/change-password', methods=["POST"])
def change_password():
    """
    Change user password.
    Accepts a JSON payload with 'old-password', 'new-password', and 'confirm-password'.
    Returns:
        str: Response message.
    """
    try:
        data = request.json
        service.change_password(
            data['old-password'], data['new-password'], data['confirm-password'])
        return make_response('Password changed', 200)
    except ServiceException as exc:
        return make_response(str(exc), 400)
    except KeyError as key_err:
        return make_response('Invalid payload :' + str(key_err), 400)
