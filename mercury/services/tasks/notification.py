# coding=utf-8

from . import celery


@celery.task()
def check_notifications():
    return 'OK TEST!'
