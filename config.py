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

    # Database
    # Handle Render's database URL format
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = database_url
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("SQLALCHEMY_DATABASE_URI could not be configured")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email Configuration
    SMTP_HOST = os.getenv('SMTP_HOST')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    SMTP_FROM_EMAIL = os.getenv('SMTP_FROM_EMAIL')

    # Email Service API
    EMAIL_SERVICE_API_KEY = os.getenv('EMAIL_SERVICE_API_KEY')
    EMAIL_SERVICE_DOMAIN = os.getenv('EMAIL_SERVICE_DOMAIN')

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
        # Validate required environment variables in production
        required_vars = [
            'SECRET_KEY',
            'DATABASE_URL',
            'JWT_SECRET_KEY',
            'PASSWORD_SALT',
            'SMTP_HOST',
            'SMTP_USERNAME',
            'SMTP_PASSWORD',
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
    # Add test-specific configurations here

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 