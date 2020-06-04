# coding=utf-8

from mercury.services.database_nosql_mongo import db as mongo

from datetime import datetime
from bson import ObjectId

from flask_restful import fields, reqparse


notification_fields = {
    'category': fields.String,
    'datetime_send': fields.String,
    # Replaces Notification ID with Notification Uri (HATEOAS) through endpoint 'notification'
    'uri': fields.Url('notification')
}


'''API Functions'''


def get_request_parser(request_parser=None):
    if request_parser is None:
        result = reqparse.RequestParser()
    else:
        result = request_parser
    result.add_argument('category', type=str, required=True, help='No notification category provided', location='json')
    result.add_argument('datetime_send', type=lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'), required=False,
                        help='No notification datetime_send provided', location='json')
    return result


def select_notification(id):
    return mongo.db.notification.find_one_or_404({'_id': ObjectId(id)})


def select_notifications():
    return mongo.db.notification.find()


def insert_notification(notification):
    return {
        '_id': mongo.db.notification.insert_one(notification).inserted_id,
        'category': notification['category'],
        'datetime_send': notification['datetime_send']
    }


def update_notification(id, notification):
    notification_found = mongo.db.notification.find_one_or_404({'_id': ObjectId(id)})
    if mongo.db.notification.update_one({'_id': notification_found['_id']}, {'$set': notification}).acknowledged:
        return {
            '_id': id,
            'category': notification['category'],
            'datetime_send': notification['datetime_send']
        }
    else:
        return {'result': False}


def delete_notification(id):
    return mongo.db.notification.remove({'_id': ObjectId(id)})['ok'] == 1.0


'''Other Functions'''


def find_notifications_to_send():
    """Find all notifications that have datetime_send lower than now (local time).

    :return: Cursor to manage notifications to send.
    """
    return mongo.db.notification.find({
        'datetime_send': {'$lt': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    })
