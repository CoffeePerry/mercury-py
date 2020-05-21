# coding=utf-8

from mercury.services.database_sql import db
from mercury.services.hashing import PASSWORD_HASH_MAX_LENGTH, hashing, bcrypt_handle_long_password

from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(254), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.Binary(PASSWORD_HASH_MAX_LENGTH), nullable=False)
    creation_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    active = db.Column(db.DateTime, nullable=False, default=False)

    def __repr__(self):
        return '<User %r>' % self.username

    @bcrypt_handle_long_password
    def hash_password(self, password):
        """
        Hash the passed plain password and save it to the user.

        :param password: The plain password.
        """
        self.password_hash = hashing.generate_password_hash(password)

    def verify_password(self, password):
        """
        Verify the passed plain password against the user's hashed password.

        :param password: The plain password to compare.
        :return: The outcome of the comparison.
        """
        return hashing.check_password_hash(self.password_hash, password)
