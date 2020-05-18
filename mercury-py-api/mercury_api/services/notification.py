# coding=utf-8

from mercury_api.models.notification import Notification
from mercury_api.services.database import db

from datetime import datetime

from flask_restful import fields, reqparse


notification_fields = {
    'datetime_send': fields.String,
    # Replaces Notification ID with Notification Uri (HATEOAS) through endpoint 'notification'
    'uri': fields.Url('notification')
}


def get_request_parser(request_parser=None):
    if request_parser is None:
        result = reqparse.RequestParser()
    else:
        result = request_parser
    result.add_argument('datetime_send', type=lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'), required=True,
                        help='No notification datetime_send provided', location='json')
    return result


def get_notification(id):
    return Notification.query.get_or_404(id)


def get_notifications():
    return Notification.query.all()


def insert_notification(new_notification):
    notification = Notification()
    [notification.__setattr__(key, value) for key, value in new_notification.items() if value is not None]
    db.session.add(notification)
    db.session.commit()
    return notification


def save_notification(notification):
    if notification is None:
        return None
    db.session.commit()
    return notification


def delete_notification(id):
    notification = Notification.query.get_or_404(id)
    db.session.delete(notification)
    db.session.commit()
    return True
