# coding=utf-8

from .services.database_sql import init_app as init_database_sql
from .services.database_nosql_mongo import init_app as init_database_nosql_mongo
from .services.hashing import init_app as init_hashing
from .services.tasks import init_app as init_tasks
from .services.tasks.notification import init_app as init_notification

import os

from flask import Flask, send_from_directory
from flask_restful import Api

__version_info__ = ('1', '0')
__version__ = '.'.join(__version_info__)

api = Api()


def create_app():
    """Application factory.

    :return: An application instance.
    """
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
    init_api(api, __version__)
    api.init_app(app)

    init_tasks(app)
    init_notification(app)

    # Base page for check if service is ready
    @app.route(f'/mercury/api/v{__version__}/')
    def index():
        """Return Mercury index page.

        :return: Mercury index page.
        """
        return f'Mercury v{__version__} online!'

    @app.route('/favicon.ico')
    def favicon():
        """Return Mercury favicon.ico.

        :return: Mercury favicon.ico.
        """
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.cli.command('info')
    def info():
        """Print Mercury info.

        :return: Mercury info.
        """
        print(f'Mercury v{__version__} ready!')

    return app
