# coding=utf-8


class Email(object):
    _host = 'localhost'
    _port = 587  # TLS default port
    _username = ''
    _password = ''

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initalizes the application with the extension.

        :param app: The Flask application object.
        """
        self._host = app.config.get('EMAIL_HOST', 'localhost')
        self._port = app.config.get('EMAIL_PORT', 587)
        self._username = app.config.get('EMAIL_USERNAME', '')
        self._password = app.config.get('EMAIL_PASSWORD', '')

    def send(self, notification):
        pass
