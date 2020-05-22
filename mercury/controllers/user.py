# coding=utf-8

from mercury.services import user as services_user

from flask import abort, request
from flask_restful import Resource, marshal


class UserListAPI(Resource):
    # decorators = []

    def __init__(self):
        self.reqparse = services_user.get_request_parser()
        super(UserListAPI, self).__init__()

    def get(self):
        return {'users': [marshal(user, services_user.user_fields) for user in services_user.select_users()]}

    def post(self):
        if not request.json:
            abort(400)
        user = {key: value for key, value in self.reqparse.parse_args().items() if value is not None}
        return {'user': marshal(services_user.insert_user(user), services_user.user_fields)}, 201


class UserAPI(Resource):
    # decorators = []

    def __init__(self):
        self.reqparse = services_user.get_request_parser()
        super(UserAPI, self).__init__()

    def get(self, id):
        return {'user': marshal(services_user.select_user(id), services_user.user_fields)}

    def put(self, id):
        if not request.json:
            abort(400)
        user = services_user.select_user(id)
        [user.__setattr__(key, value) for key, value in self.reqparse.parse_args().items() if value is not None]
        return {'user': marshal(services_user.update_user(user), services_user.user_fields)}

    def delete(self, id):
        return {'result': services_user.delete_user(id)}
