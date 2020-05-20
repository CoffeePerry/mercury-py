# coding=utf-8

# from mercury.models.notification import Notification
from mercury.services.database import db
from mercury.services.hashing import hashing

from datetime import datetime
from typing import Final


class User(db.Model):
    _PASSWORD_HASH_MAX_LENGTH: Final = 72

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(254), index=True)
    password_hash = db.Column(db.Binary(_PASSWORD_HASH_MAX_LENGTH))

    def hash_password(self, password):
        if password > self._PASSWORD_HASH_MAX_LENGTH:
            raise Exception('Field "password" length can\'t be greater than ' + str(self._PASSWORD_HASH_MAX_LENGTH))
        # self.password_hash = hashing #pwd_context.encrypt(password)

    def verify_password(self, password):
        pass
        # return pwd_context.verify(password, self.password_hash)
