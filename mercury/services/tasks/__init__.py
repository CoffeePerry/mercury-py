# coding=utf-8

from celery import Celery

celery = Celery(__name__)


def init_app(app):
    celery.conf.broker_url = app.config['BROKER_URL']
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
