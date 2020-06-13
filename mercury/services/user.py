# coding=utf-8

from mercury.models.user import User
from mercury.services.database_sql import db

from flask_restful import fields, reqparse

"""Fields to marshal user to JSON."""
user_fields = {
    'username': fields.String,
    'creation_datetime': fields.String,
    'active': fields.Boolean,
    'uri': fields.Url('user')  # Replaces User ID with User Uri (HATEOAS) through endpoint 'user'
}


def get_request_parser(request_parser=None):
    """Get request parser for user.

    :param request_parser: If exists, add request parser argument to request_parser param.
    :return: User request parser.
    """
    if request_parser is None:
        result = reqparse.RequestParser()
    else:
        result = request_parser
    result.add_argument('username', type=str, required=True, help='No user username provided', location='json')
    result.add_argument('password', type=str, required=True, help='No user password provided', location='json')
    return result


'''API Functions'''


def select_user(id):
    """Get user by id param.

    :param id: User's id to find.
    :return: User found.
    """
    return User.query.get_or_404(id)


def select_users():
    """Get all users.

    :return: All users.
    """
    return User.query.all()


def insert_user(new_user):
    """Post the user passed by new_user param.

    :param new_user: User to persist.
    :return: Persisted user or error.
    """
    user = User()
    [user.__setattr__(key, value) for key, value in new_user.items() if value is not None]
    user.hash_password(user.password)
    db.session.add(user)
    db.session.commit()
    return user


def update_user(user):
    """Put the user passed by user param.

    :param user: User to persist.
    :return: Persisted user or error.
    """
    if user is None:
        return None
    db.session.commit()
    return user


def delete_user(id):
    """Delete the user that have the passed user id.

    :param id: User's id to find.
    :return: True if elimination was successful or False if elimination was not possible.
    """
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return True
