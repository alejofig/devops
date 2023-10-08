import uuid
from app import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    app_uuid = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    blocked_reason = db.Column(db.String(255))
    datetime_request = db.Column(db.DateTime, nullable=False)
    ip_request = db.Column(db.String(15), nullable=False)

    def __init__(self, app_uuid, email, blocked_reason, datetime_request, ip_request):
        self.app_uuid = app_uuid
        self.email = email
        self.blocked_reason = blocked_reason
        self.datetime_request = datetime_request
        self.ip_request = ip_request
