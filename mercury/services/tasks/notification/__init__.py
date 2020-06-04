# coding=utf-8

from .email import Email
from .. import celery
from mercury.services.notification import find_notifications_to_send

email = Email()


def init_app(app):
    """Initalizes the application with the extension.

    :param app: The Flask application object.
    """
    email.init_app(app)


def route_notification(notification):
    return {
        'email': email.send(notification)
    }.get(notification['category'], 'email')


@celery.task()
def route_notifications():
    return 'OK'
    notifications = find_notifications_to_send()
    if notifications is None:
        return 'Nothing to send.'
    for notification in notifications:
        self.route_notification(notification)
