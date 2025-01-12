from datetime import datetime
from . import db

class Newsletter(db.Model):
    __tablename__ = 'newsletters'
    
    newsletter_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    topic = db.Column(db.String(100))
    subject = db.Column(db.String(255))
    body = db.Column(db.Text)
    date_received = db.Column(db.DateTime, default=datetime.utcnow)
    summary = db.Column(db.Text)

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    settings = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    newsletters = db.relationship('Newsletter', backref='user', lazy=True)
    digests = db.relationship('Digest', backref='user', lazy=True)

class Digest(db.Model):
    __tablename__ = 'digests'
    
    digest_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.JSON) 