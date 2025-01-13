from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Initialize Mailgun service
    from app.services.mailgun import MailgunService
    mailgun = MailgunService()
    mailgun.init_app(app)
    
    # Register blueprints
    from app.routes.webhooks import webhooks
    app.register_blueprint(webhooks, url_prefix='')
    
    @app.route('/')
    def index():
        return 'Newsletter Aggregator API'
    
    return app

# Create the application instance
app = create_app('production')

# Import models after app creation to avoid circular imports
from app.models import User, Newsletter, Digest

# Push an application context
app_context = app.app_context()
app_context.push() 