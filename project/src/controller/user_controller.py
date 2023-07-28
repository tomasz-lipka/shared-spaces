from flask import Blueprint, request, make_response

from exception.service_exception import ServiceException
import service.user_service as service

user_controller = Blueprint('user_controller', __name__)


@user_controller.route('/login', methods=["POST"])
def login():
    """Endpoint for user log-in"""
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
    """Endpoint for user registration"""
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
    """Endpoint for user logout"""
    service.logout()
    return make_response('Logged out', 200)


@user_controller.route('/change-password', methods=["POST"])
def change_password():
    """Endpoint to change the password"""
    try:
        data = request.json
        service.change_password(
            data['old-password'], data['new-password'], data['confirm-password'])
        return make_response('Password changed', 200)
    except ServiceException as exc:
        return make_response(str(exc), 400)
    except KeyError as key_err:
        return make_response('Invalid payload :' + str(key_err), 400)
