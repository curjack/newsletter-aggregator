from datetime import datetime
from app import db

class Digest(db.Model):
    __tablename__ = 'digests'
    
    digest_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.JSON) 