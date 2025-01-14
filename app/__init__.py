from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    """Application factory function."""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    
    # Load config
    from config import config
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes.webhooks import webhooks
    app.register_blueprint(webhooks)

    # Register CLI commands
    from app.cli import register_commands
    register_commands(app)

    @app.route('/')
    def index():
        return 'Newsletter Aggregator API'

    return app

# Create a global instance for Gunicorn
app = create_app('production') 