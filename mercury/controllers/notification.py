# coding=utf-8

from mercury.services import notification as services_notification
from mercury.services.database import create_db  # Test

from flask import abort, request
from flask_restful import Resource, marshal


class NotificationListAPI(Resource):
    # decorators = [AuthHmac.get_instance().auth()]

    def __init__(self):
        self.reqparse = services_notification.get_request_parser()
        super(NotificationListAPI, self).__init__()

    def get(self):
        create_db()  # Test
        return {'notifications': [marshal(notification, services_notification.notification_fields) for notification
                                  in services_notification.get_notifications()]}

    def post(self):
        if not request.json:
            abort(400)
        notification = {key: value for key, value in self.reqparse.parse_args().items() if value is not None}
        return {'notification': marshal(services_notification.insert_notification(notification),
                                        services_notification.notification_fields)}, 201  # 201 = Code for "Created"


class NotificationAPI(Resource):
    # decorators = [AuthHmac.get_instance().auth()]

    def __init__(self):
        self.reqparse = services_notification.get_request_parser()
        super(NotificationAPI, self).__init__()

    def get(self, id):
        return {'notification': marshal(services_notification.get_notification(id),
                                        services_notification.notification_fields)}

    def put(self, id):
        if not request.json:
            abort(400)
        notification = services_notification.get_notification(id)
        [notification.__setattr__(key, value) for key, value in self.reqparse.parse_args().items() if value is not None]
        return {'notification': marshal(services_notification.save_notification(notification),
                                        services_notification.notification_fields)}

    def delete(self, id):
        return {'result': services_notification.delete_notification(id)}
