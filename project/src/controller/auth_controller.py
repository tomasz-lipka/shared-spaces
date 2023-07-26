from flask import Blueprint, request, make_response
from flask_login import login_user, logout_user, current_user, login_required
from exception.service_exception import ServiceException
import service.user_service as service

auth_controller = Blueprint('auth_controller', __name__)


@auth_controller.route('/login', methods=["POST"])
def login():
    """Endpoint for user log-in"""
    data = request.json
    try:
        user = service.get_verified_user(data['login'], data['password'])
        if user:
            login_user(user)
            return make_response('Loged in', 200)
        return make_response('Wrong login and/or password', 401)
    except KeyError as key_err:
        return make_response('Invalid payload :' + str(key_err), 409)


@auth_controller.route('/register', methods=["POST"])
def register():
    """Register a new user"""
    data = request.json
    try:
        service.create_user(
            data['login'], data['password'], data['confirm-password'])
        return make_response('User created', 200)
    except ServiceException as exc:
        return make_response(str(exc), 409)
    except KeyError as key_err:
        return make_response('Invalid payload :' + str(key_err), 409)


@auth_controller.route('/logout')
def logout():
    """Allows the user to end his session"""
    logout_user()
    return make_response('Logged out', 200)


@auth_controller.route('/change-password', methods=["POST"])
@login_required
def change_password():
    # TODO
    """Endpoint to change the password"""
    data = request.json
    user = repository.get_user_by_id(current_user.get_id())
    user.change_password(data['new-password'])
    repository.update_user(user)
    return make_response('Password changed', 200)
