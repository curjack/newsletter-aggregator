from app import create_app
from flask import current_app
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_app_context():
    """Test application context and configuration."""
    app = create_app('development')
    
    # Test 1: Outside app context
    logger.info("Testing outside app context...")
    try:
        print(current_app)
    except RuntimeError as e:
        logger.info(f"Expected error outside context: {e}")
    
    # Test 2: Inside app context
    logger.info("Testing inside app context...")
    with app.app_context():
        # Now we can access current_app
        logger.info(f"Current app name: {current_app.name}")
        logger.info(f"Database URL: {current_app.config['SQLALCHEMY_DATABASE_URI']}")
        logger.info(f"Environment: {current_app.config['FLASK_ENV']}")

if __name__ == '__main__':
    test_app_context() 