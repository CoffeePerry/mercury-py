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
    result.add_argument('password', type=str, required=True, help='No user password provided', location='json')
    return result


def select_user(id):
    return User.query.get_or_404(id)


def select_users():
    return User.query.all()


def insert_user(new_user):
    user = User()
    [user.__setattr__(key, value) for key, value in new_user.items() if value is not None]
    user.hash_password(user.password)
    db.session.add(user)
    db.session.commit()
    return user


def update_user(user):
    if user is None:
        return None
    db.session.commit()
    return user


def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return True
