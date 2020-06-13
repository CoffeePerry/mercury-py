# coding=utf-8

from mercury.controllers.notification import NotificationListAPI, NotificationAPI
from mercury.controllers.user import UserListAPI, UserAPI


def init_api(api, version='0.0'):
    """Initalizes the application Api routes.

    :param api: The Flask application's Api object.
    :param version: The Flask application's version (default is 0.0).
    """
    api.add_resource(NotificationListAPI, f'/mercury/api/v{version}/notifications/', endpoint='notifications')
    api.add_resource(NotificationAPI, f'/mercury/api/v{version}/notifications/<string:_id>',
                     endpoint='notification')
    api.add_resource(UserListAPI, f'/mercury/api/v{version}/users/', endpoint='users')
    api.add_resource(UserAPI, f'/mercury/api/v{version}/users/<int:id>', endpoint='user')
