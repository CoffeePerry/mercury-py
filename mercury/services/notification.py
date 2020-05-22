# coding=utf-8

from mercury.services.database_nosql_mongo import db as mongo

from datetime import datetime
from bson import ObjectId

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


def select_notification(id):
    return mongo.db.notification.find_one_or_404({'_id': ObjectId(id)})


def select_notifications():
    return mongo.db.notification.find()


def insert_notification(notification):
    return {
        '_id': mongo.db.notification.insert_one(notification).inserted_id,
        'datetime_send': notification['datetime_send']
    }


def update_notification(id, notification):
    if mongo.db.notification.update_one({'_id': ObjectId(id)}, {'$set': notification}).acknowledged:
        return {
            '_id': id,
            'datetime_send': notification['datetime_send']
        }
    else:
        return {'result': False}


def delete_notification(id):
    return mongo.db.notification.remove({'_id': ObjectId(id)})['ok'] == 1.0
