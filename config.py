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
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:///dev.db'  # fallback to SQLite
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
        super().__init__()
        if not os.getenv('DATABASE_URL'):
            raise ValueError("Production environment requires DATABASE_URL to be set")
        
        # Validate other required environment variables
        required_vars = [
            'SECRET_KEY',
            'JWT_SECRET_KEY',
            'PASSWORD_SALT',
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
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 