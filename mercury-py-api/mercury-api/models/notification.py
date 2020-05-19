# coding=utf-8

from ..services.database import db

from datetime import datetime


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime_send = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Notification %r>' % str(self.id)
