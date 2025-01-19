from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import logging

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app(config_name=None):
    """Application factory function."""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    
    # Load config
    from config import config
    app.config.from_object(config[config_name])

    # Log configuration for debugging
    logger.info(f"Initializing app in {config_name} mode")
    logger.info(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize services
    from app.services.mailgun import MailgunService
    mailgun = MailgunService()
    mailgun.init_app(app)

    # Register blueprints
    from app.routes.webhooks import webhooks
    app.register_blueprint(webhooks)

    # Register CLI commands
    from app.cli import register_commands
    register_commands(app)

    @app.route('/')
    def index():
        return 'Newsletter Aggregator API'

    # Register error handlers
    @app.errorhandler(500)
    def handle_500(error):
        logger.error(f"Internal Server Error: {error}")
        return {
            'status': 'error',
            'message': 'Internal Server Error',
            'error': str(error)
        }, 500

    @app.errorhandler(404)
    def handle_404(error):
        return {
            'status': 'error',
            'message': 'Not Found',
            'error': str(error)
        }, 404

    return app

# Create a global instance for Gunicorn
app = create_app('production') 