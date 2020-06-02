# coding=utf-8

"""
Work in progress.

TODO:
- Auth;
"""

from .services.database_sql import init_app as init_database_sql
from .services.database_nosql_mongo import init_app as init_database_nosql_mongo
from .services.hashing import init_app as init_hashing
from .services.tasks import init_app as init_tasks

import os

from flask import Flask
from flask_restful import Api

api = Api()


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(app.instance_path, "mercury.sqlite3")}'
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

    init_database_sql(app)
    init_database_nosql_mongo(app)
    init_hashing(app)

    # Load routes after load other services
    from .services.routes import init_api
    init_api(api)
    api.init_app(app)

    init_tasks(app)

    # Base page for check if service is ready
    @app.route('/mercury/api/v1.0/')
    def index():
        return 'Mercury v1.0 online!'

    @app.cli.command('info')
    def info():
        print('Mercury v1.0 ready!')

    return app
