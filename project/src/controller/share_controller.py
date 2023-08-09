from flask import Blueprint, request, make_response
import json

from ..exception.service_exception import ServiceException
from ..service import share_service as service

share_controller = Blueprint('share_controller', __name__)


@share_controller.route('/spaces/<int:space_id>/shares', methods=["POST"])
def post_share(space_id):
    try:
        data = request.json
        service.create_share(space_id, data['text'])
        return make_response('Share created', 200)
    except ServiceException as exc:
        return make_response(str(exc), 400)
    except KeyError as key_err:
        return make_response('Invalid payload :' + str(key_err), 400)


@share_controller.route('/shares/<int:share_id>')
def get_share(share_id):
    try:
        share = service.get_share_by_share_id(share_id)
        return json.dumps(share.to_dict())
    except ServiceException as exc:
        return make_response(str(exc), 400)


@share_controller.route('/spaces/<int:space_id>/shares')
def get_shares(space_id):
    try:
        shares = service.get_shares_by_space_id(space_id)
        json_serializable_list = [share.shares_to_dict() for share in shares]
        return json.dumps(json_serializable_list)
    except ServiceException as exc:
        return make_response(str(exc), 400)


@share_controller.route('/shares/<int:share_id>', methods=["DELETE"])
def delete_share(share_id):
    try:
        service.delete_share_by_share_id(share_id)
        return make_response('Share deleted', 200)
    except ServiceException as exc:
        return make_response(str(exc), 400)


@share_controller.route('/shares/<int:share_id>', methods=["PUT"])
def put_share(share_id):
    try:
        data = request.json
        service.edit_share(share_id, data['text'])
        return make_response('Share edited', 200)
    except ServiceException as exc:
        return make_response(str(exc), 400)
    except KeyError as key_err:
        return make_response('Invalid payload :' + str(key_err), 400)
