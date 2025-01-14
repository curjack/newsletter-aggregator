from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config['production']())

# Initialize extensions
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

# Push application context
app.app_context().push()

# Import models
from app.models import User, Newsletter, Digest

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