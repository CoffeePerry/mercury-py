# coding=utf-8

from flask_bcrypt import Bcrypt

hashing = Bcrypt()


def init_app(app):
    hashing.init_app(app)
