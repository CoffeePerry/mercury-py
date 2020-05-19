# coding=utf-8

from ..controllers.notification import NotificationListAPI, NotificationAPI


def init_api(api):
    api.add_resource(NotificationListAPI, '/mercury/api/v1.0/notifications/', endpoint='notifications')
    api.add_resource(NotificationAPI, '/mercury/api/v1.0/notifications/<int:id>', endpoint='notification')
