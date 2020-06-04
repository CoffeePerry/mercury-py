# coding=utf-8

'''Work in progress.

TODO:
- Auth, with registration by CLI;
'''

from .services.database_sql import init_app as init_database_sql
from .services.database_nosql_mongo import init_app as init_database_nosql_mongo
from .services.hashing import init_app as init_hashing
from .services.tasks import init_app as init_tasks
from .services.tasks.notification import init_app as init_notification

import os

from flask import Flask
from flask_restful import Api

api = Api()


def create_app():
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Ensure the instance folder exists
    try:
        if not os.path.isdir(app.instance_path):
            os.makedirs(app.instance_path)
            raise Exception('Directory not found, so just created. Put file "config.py" inside, please.')
    except OSError:
        pass  # TODO: Log

    from instance.config import ProductionConfig, DevelopmentConfig
    if app.env == 'production':
        app.config.from_object(ProductionConfig(app))  # Load the production instance config
    else:
        app.config.from_object(DevelopmentConfig(app))  # Load the development instance config

    init_database_sql(app)
    init_database_nosql_mongo(app)
    init_hashing(app)

    # Load routes after load other services
    from .services.routes import init_api
    init_api(api)
    api.init_app(app)

    init_tasks(app)
    init_notification(app)

    # Base page for check if service is ready
    @app.route('/mercury/api/v1.0/')
    def index():
        return 'Mercury v1.0 online!'

    @app.cli.command('info')
    def info():
        print('Mercury v1.0 ready!')

    return app
