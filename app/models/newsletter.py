from datetime import datetime
from app import db

class Newsletter(db.Model):
    __tablename__ = 'newsletters'
    
    newsletter_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    topic = db.Column(db.String(100))
    subject = db.Column(db.String(255))
    body = db.Column(db.Text)
    date_received = db.Column(db.DateTime, default=datetime.utcnow)
    summary = db.Column(db.Text) 