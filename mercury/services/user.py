# coding=utf-8

from mercury.models.user import User
from mercury.services.database_sql import db

from datetime import datetime

from flask_restful import fields, reqparse


user_fields = {
    'username': fields.String,
    'creation_datetime': fields.String,
    'active': fields.Boolean,
    'uri': fields.Url('user')  # Replaces User ID with User Uri (HATEOAS) through endpoint 'user'
}


def get_request_parser(request_parser=None):
    if request_parser is None:
        result = reqparse.RequestParser()
    else:
        result = request_parser
    result.add_argument('username', type=str, required=True, help='No user username provided', location='json')
    result.add_argument('creation_datetime', type=lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'), required=True,
                        help='No user creation_datetime provided', location='json')
    result.add_argument('active', type=bool, required=True, help='No user active provided', location='json')
    return result


def get_user(id):
    return User.query.get_or_404(id)


def get_users():
    return User.query.all()


def insert_user(new_user):
    user = User()
    [user.__setattr__(key, value) for key, value in new_user.items() if value is not None]
    db.session.add(user)
    db.session.commit()
    return user


def save_user(user):
    if user is None:
        return None
    db.session.commit()
    return user


def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return True
