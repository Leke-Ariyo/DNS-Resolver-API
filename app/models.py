from app import db
from datetime import datetime


class DNSQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(255), nullable=False)
    client_ip = db.Column(db.String(255))
    addresses = db.Column(db.String(1024))
    created_time = db.Column(
        db.Integer,
        default=lambda: int(datetime.utcnow().timestamp())
    )
