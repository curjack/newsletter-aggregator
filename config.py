import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration."""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'

    # Database Configuration
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL must be set")
    
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mailgun Configuration
    MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
    MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
    MAILGUN_BASE_URL = os.getenv('MAILGUN_BASE_URL', 'https://api.mailgun.net/v3')
    MAILGUN_WEBHOOK_SIGNING_KEY = os.getenv('MAILGUN_WEBHOOK_SIGNING_KEY')
    
    # Newsletter receiving email
    NEWSLETTER_RECEIVING_EMAIL = os.getenv('NEWSLETTER_RECEIVING_EMAIL', 'newsletters@{domain}')
    
    # Digest sending configuration
    DIGEST_FROM_EMAIL = os.getenv('DIGEST_FROM_EMAIL', 'digests@{domain}')
    DIGEST_FROM_NAME = os.getenv('DIGEST_FROM_NAME', 'Newsletter Digest')

    # Security
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-change-in-production')
    PASSWORD_SALT = os.getenv('PASSWORD_SALT', 'salt-change-in-production')

    # Application Settings
    APP_NAME = os.getenv('APP_NAME', 'Newsletter Aggregator')
    APP_URL = os.getenv('APP_URL', 'http://localhost:5000')
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:5000').split(',')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    
    def __init__(self):
        super().__init__()
        
        # Validate other required environment variables
        required_vars = [
            'SECRET_KEY',
            'JWT_SECRET_KEY',
            'PASSWORD_SALT',
            'MAILGUN_API_KEY',
            'MAILGUN_DOMAIN',
            'MAILGUN_WEBHOOK_SIGNING_KEY'
        ]
        
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    # Use a test database URL instead of in-memory SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or os.environ.get('DATABASE_URL')

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 