# coding=utf-8

from os import path


class DevelopmentConfig(object):
    def __init__(self, app=None):
        """DevelopmentConfig constructor.

        :param app: Application in which to inject the development settings.
        """
        self.app = app

        # Flask
        self.SECRET_KEY = ''

        # Flask-JWT-Extended
        self.JWT_SECRET_KEY = self.SECRET_KEY

        # DBs
        self.DATABASE_FILENAME = path.join(self.app.instance_path, "sqldb", "mercury.sqlite3")
        self.SQLALCHEMY_DATABASE_URI = f'sqlite:///{self.DATABASE_FILENAME}'
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.MONGO_URI = 'mongodb://localhost:27017/mercury'

        # Celery - for Tasks
        self.BROKER_URL = 'amqp://developer:devrabbit@localhost:5672/mercury'
        self.CELERY_RESULT_BACKEND = self.MONGO_URI

        # Email
        self.MAIL_SERVER = 'smtp.gmail.com'
        self.MAIL_PORT = 587
        self.MAIL_USE_TLS = True
        self.MAIL_USERNAME = ''
        self.MAIL_PASSWORD = ''  # Gmail App Password
        self.MAIL_DEFAULT_SENDER = ('', '')


class ProductionConfig(object):
    def __init__(self, app=None):
        """ProductionConfig constructor.

        :param app: Application in which to inject the production settings.
        """
        self.app = app

        # Flask
        self.SECRET_KEY = ''

        # Flask-JWT-Extended
        self.JWT_SECRET_KEY = self.SECRET_KEY

        # DBs
        self.DATABASE_FILENAME = path.join(self.app.instance_path, "sqldb", "mercury.sqlite3")
        self.SQLALCHEMY_DATABASE_URI = f'sqlite:///{self.DATABASE_FILENAME}'
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.MONGO_URI = 'mongodb://localhost:27017/mercury'

        # Celery - for Tasks
        self.BROKER_URL = 'amqp://developer:devrabbit@localhost:5672/mercury'
        self.CELERY_RESULT_BACKEND = self.MONGO_URI

        # Email
        self.MAIL_SERVER = 'smtp.gmail.com'
        self.MAIL_PORT = 587
        self.MAIL_USE_TLS = True
        self.MAIL_USERNAME = ''
        self.MAIL_PASSWORD = ''  # Gmail App Password
        self.MAIL_DEFAULT_SENDER = ('', '')
