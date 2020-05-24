# coding=utf-8

from flask_sqlalchemy import SQLAlchemy
from flask.cli import AppGroup

db = SQLAlchemy()
db_cli = AppGroup('database')


def init_app(app):
    """
    Initalizes the application database (SQL).

    :param app: The Flask application object.
    """
    db.init_app(app)
    app.cli.add_command(db_cli)


@db_cli.command('create')
def create_database():
    create_db()
    print('Database SQL created')


@db_cli.command('drop')
def create_database():
    response = input('Are you really sure to delete the SQL database and all the data it contains? [Y/n]:')
    if response == 'Y':
        drop_db()
        print('Database SQL dropped')


def create_db():
    """
    Create the database schema.
    """
    db.create_all()

def drop_db():
    """
    Drop the database.
    """
    db.drop_all()
