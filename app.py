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
    
    # Load config
    app.config.from_object(config[config_name])

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes.webhooks import webhooks
    app.register_blueprint(webhooks)

    @app.route('/')
    def index():
        return 'Newsletter Aggregator API'

    return app

# Create a global instance for Gunicorn to use
app = create_app('production')

if __name__ == '__main__':
    app.run() 