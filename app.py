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
    
    # Debug: Print environment variables
    print("DEBUG: Environment variables:")
    print(f"FLASK_ENV: {os.getenv('FLASK_ENV')}")
    print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
    
    # Load config
    app.config.from_object(config[config_name])
    
    # Debug: Print final configuration
    print("DEBUG: Final configuration:")
    print(f"SQLALCHEMY_DATABASE_URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)

    # Register models
    from models import User, Newsletter, Digest

    return app

# Create app instance
app = create_app()

@app.route('/')
def index():
    return 'Newsletter Aggregator API'

if __name__ == '__main__':
    app.run() 