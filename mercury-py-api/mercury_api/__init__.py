# coding=utf-8

from mercury_api.services.database import db

import os

from flask import Flask
from flask_restful import Api


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(app.instance_path, "mercury.sqlite3")}',
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # --- Necessary to correctly create database schema
    import mercury_api.models.notification
    # ---
    with app.app_context():
        db.init_app(app)
        db.create_all()

    api = Api(app)

    from mercury_api.controllers.notification import NotificationListAPI, NotificationAPI
    api.add_resource(NotificationListAPI, '/mercury/api/v1.0/notifications/', endpoint='notifications')
    api.add_resource(NotificationAPI, '/mercury/api/v1.0/notifications/<int:id>', endpoint='notification')

    # Base page for check if service is ready
    @app.route('/mercury/api/v1.0/')
    def index():
        return 'Mercury v1.0 online!'

    return app
