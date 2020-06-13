# coding=utf-8

from hashlib import sha256
from functools import wraps

from flask_bcrypt import Bcrypt


hashing = Bcrypt()


def init_app(app):
    """Initalizes the application hashing.

    :param app: The Flask application object.
    """
    hashing.init_app(app)


def bcrypt_handle_long_password(function):
    """Decorator to handle long password for bcrypt hashing."""
    @wraps(function)
    def wrapper(*args, **kwargs):
        user, password = args
        if password is None:
            raise Exception('Parameter password can\'t be None')
        password = sha256(password.encode('utf-8')).hexdigest()
        password = unicode_to_bytes(password)
        return function(user, password, **kwargs)
    return wrapper


def unicode_to_bytes(unicode_string):
    """Converts a Unicode string to a bytes object.

    :param unicode_string: The Unicode string to convert.
    :return: The bytes object converted from the Unicode string.
    """
    if isinstance(unicode_string, str):
        bytes_object = bytes(unicode_string, 'utf-8')
    else:
        bytes_object = unicode_string
    return bytes_object
