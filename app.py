from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    """Application factory function."""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)

    # Register models
    from models import User, Newsletter, Digest  # We'll create this file next

    return app

# Create app instance
app = create_app()

# Models
class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    settings = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    newsletters = db.relationship('Newsletter', backref='user', lazy=True)
    digests = db.relationship('Digest', backref='user', lazy=True)

class Newsletter(db.Model):
    __tablename__ = 'newsletters'
    
    newsletter_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    topic = db.Column(db.String(100))
    subject = db.Column(db.String(255))
    body = db.Column(db.Text)
    date_received = db.Column(db.DateTime, default=datetime.utcnow)
    summary = db.Column(db.Text)

class Digest(db.Model):
    __tablename__ = 'digests'
    
    digest_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.JSON)

@app.route('/')
def index():
    return 'Newsletter Aggregator API'

if __name__ == '__main__':
    app.run() 