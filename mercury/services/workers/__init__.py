# coding=utf-8

from celery import Celery

celery = Celery()
# celery = Celery(__name__, broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


def init_app(app):
    my_celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    my_celery.conf.update(app.config)

    class ContextTask(my_celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    my_celery.Task = ContextTask
    return my_celery


@celery.task()
def test(a, b):
    return a + b
