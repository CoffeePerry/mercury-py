# coding=utf-8

from mercury import create_app
from mercury.services.workers import celery

app = create_app()
# app.app_context().push()
app.conf.imports = app.conf.imports + 'mercury.services.workers'
