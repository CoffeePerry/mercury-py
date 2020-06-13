# coding=utf-8

from mercury.services import notification as services_notification

from flask import abort, request
from flask_restful import Resource, marshal


class NotificationListAPI(Resource):
    # decorators = []

    def __init__(self):
        """NotificationListAPI constructor."""
        self.reqparse = services_notification.get_request_parser()
        super(NotificationListAPI, self).__init__()

    def get(self):
        """GET

        :return: All notifications.
        """
        return {'notifications': [marshal(notification, services_notification.notification_fields) for notification
                                  in services_notification.select_notifications()]}

    def post(self):
        """POST

        :return: Persisted notification's base informations as JSON or error.
        """
        if not request.json:
            abort(400)
        return {'notification': marshal(services_notification.insert_notification(request.json),
                                        services_notification.notification_fields)}, 201


class NotificationAPI(Resource):
    # decorators = []

    def __init__(self):
        """NotificationAPI constructor."""
        self.reqparse = services_notification.get_request_parser()
        super(NotificationAPI, self).__init__()

    def get(self, _id):
        """GET

        :param _id: Notification's id to find.
        :return: Notification found as JSON.
        """
        return {'notification': marshal(services_notification.select_notification(_id),
                                        services_notification.notification_fields)}

    def put(self, _id):
        """PUT

        :param _id: Notification's id to find.
        :return: Persisted notification's base informations as JSON or error.
        """
        if not request.json:
            abort(400)
        result = services_notification.update_notification(_id, request.json)
        if result is None:
            return {'result': False}
        return {'notification': marshal(result, services_notification.notification_fields)}

    def delete(self, _id):
        """DELETE

        :param _id: Notification's id to find.
        :return: True if elimination was successful or False if elimination was not possible.
        """
        return {'result': services_notification.delete_notification(_id)}
