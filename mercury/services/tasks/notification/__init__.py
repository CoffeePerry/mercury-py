# coding=utf-8

# TODO: Re-generate requirements.txt adding Flask-Mail

from .. import celery
from mercury.services.notification import find_notifications_to_send

from flask_mail import Mail, Message

mail = Mail()


def init_app(app):
    """Initalizes the application with the extension.

    :param app: The Flask application object.
    """
    mail.init_app(app)


def route_notification(notification):
    return {
        'email': route_notification_mail(notification)
    }.get(notification['category'], 'email')


def route_notification_mail(notification):
    msg = Message(notification['text'], recipients=notification['recipients'])
    mail.send(msg)


@celery.task()
def route_notifications():
    notifications = find_notifications_to_send()
    if notifications is None:
        return 'Nothing to send.'
    for notification in notifications:
        route_notification(notification)
