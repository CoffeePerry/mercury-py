# coding=utf-8

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    """
    Initalizes the application database (SQL).

    :param app: The Flask application object.
    """
    db.init_app(app)


def create_db():
    """
    Create the database schema.
    """
    db.create_all()
