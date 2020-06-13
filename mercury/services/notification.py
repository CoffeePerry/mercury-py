# coding=utf-8

from mercury.services.database_nosql_mongo import db as mongo

from datetime import datetime
from bson import ObjectId

from flask_restful import fields, reqparse

"""Fields to marshal notification to JSON."""
notification_fields = {
    'category': fields.String,
    'datetime_schedule': fields.String,
    'datetime_dispatch': fields.String,
    # Replaces Notification ID with Notification Uri (HATEOAS) through endpoint 'notification'
    'uri': fields.Url('notification')
}


'''API Functions'''


def get_request_parser(request_parser=None):
    """Get request parser for notification.

    :param request_parser: If exists, add request parser argument to request_parser param.
    :return: Notification request parser.
    """
    if request_parser is None:
        result = reqparse.RequestParser()
    else:
        result = request_parser
    result.add_argument('category', type=str, required=True, help='No notification category provided', location='json')
    result.add_argument('datetime_schedule', type=lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'), required=False,
                        help='No notification datetime_schedule provided', location='json')
    return result


def select_notification(id):
    """Get notification by id param.

    :param id: Notification's id to find.
    :return: Notification found or error 404.
    """
    return mongo.db.notification.find_one_or_404({'_id': ObjectId(id)})


def select_notifications():
    """Get all notifications.

    :return: All notifications.
    """
    return mongo.db.notification.find()


def insert_notification(notification):
    """Post the notification passed by notification param (MongoDB has limit of 16 megabytes per document).

    :param notification: Notification to persist.
    :return: Persisted notification's base informations or error.
    """
    return {
        '_id': mongo.db.notification.insert_one(notification).inserted_id,
        'category': notification['category'],
        'datetime_schedule': notification['datetime_schedule']
    }


def update_notification(id, notification):
    """Put the notification passed by notification param (MongoDB has limit of 16 megabytes per document).

    :param id: Notification's id to find.
    :param notification: Notification to persist.
    :return: Persisted notification's base informations or error.
    """
    notification_found = mongo.db.notification.find_one_or_404({'_id': ObjectId(id)})
    if mongo.db.notification.update_one({'_id': notification_found['_id']}, {'$set': notification}).acknowledged:
        return {
            '_id': id,
            'category': notification['category'],
            'datetime_schedule': notification['datetime_schedule']
        }
    else:
        return None


def delete_notification(id):
    """Delete the notification that have the passed notification id.

    :param id: Notification's id to find.
    :return: True if elimination was successful or False if elimination was not possible.
    """
    return mongo.db.notification.remove({'_id': ObjectId(id)})['ok'] == 1.0


'''Other Functions'''


def find_notifications_to_dispatch():
    """Find all notifications that have datetime_schedule lower than now (local time) and that they haven't already been
     dispatched.

    :return: Cursor to manage notifications to dispatch.
    """
    return mongo.db.notification.find({
        'datetime_schedule': {'$lte': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
        'datetime_dispatch': None
    })
