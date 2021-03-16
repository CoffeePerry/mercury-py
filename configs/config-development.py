# coding=utf-8

DEBUG = True

# Flask
SECRET_KEY = 'dev'

# Flask-JWT-Extended
JWT_SECRET_KEY = SECRET_KEY

# DBs
MONGO_URI = 'mongodb://localhost:27017/mercury'

# Celery - for Tasks
BROKER_URL = 'amqp://[USERNAME]:[PASSWORD]@localhost:5672/mercury'
CELERY_RESULT_BACKEND = MONGO_URI

# Email
MAIL_SERVER = ''
MAIL_PORT = -1
MAIL_USE_TLS = True
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = ('', '')
