from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    settings = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    newsletters = db.relationship('Newsletter', backref='user', lazy=True)
    digests = db.relationship('Digest', backref='user', lazy=True) 