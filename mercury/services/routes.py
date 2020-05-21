# coding=utf-8

from mercury.controllers.notification import NotificationListAPI, NotificationAPI
from mercury.controllers.user import UserListAPI, UserAPI


def init_api(api):
    """
    Initalizes the application Api routes.

    :param api: The Flask application's Api object.
    """
    api.add_resource(NotificationListAPI, '/mercury/api/v1.0/notifications/', endpoint='notifications')
    api.add_resource(NotificationAPI, '/mercury/api/v1.0/notifications/<int:id>', endpoint='notification')
    api.add_resource(UserListAPI, '/mercury/api/v1.0/users/', endpoint='users')
    api.add_resource(UserAPI, '/mercury/api/v1.0/users/<int:id>', endpoint='user')
