from flask import Blueprint, request, jsonify, current_app
import logging
from datetime import datetime
import time
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models import Newsletter, User, classify_newsletter, extract_summary
from app.services.mailgun import MailgunService

webhooks = Blueprint('webhooks', __name__)
logger = logging.getLogger(__name__)

# Constants
SYSTEM_USER_EMAIL = 'system@newsletter-aggregator.com'

def get_or_create_system_user():
    """Get the system user ID, creating it if it doesn't exist."""
    system_user = User.query.filter_by(email=SYSTEM_USER_EMAIL).first()
    if not system_user:
        logger.warning('System user not found, creating it')
        system_user = User(
            email=SYSTEM_USER_EMAIL,
            password_hash='not_used_for_system_user',
            created_at=datetime.utcnow()
        )
        db.session.add(system_user)
        db.session.commit()
    return system_user

@webhooks.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    try:
        # Verify database connection
        db.session.execute('SELECT 1')
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@webhooks.route('/webhooks/mailgun', methods=['POST', 'GET'])
def handle_mailgun_webhook():
    """Handle incoming emails from Mailgun."""
    logger.info('=' * 80)
    logger.info('Received request to /webhooks/mailgun')
    logger.info(f'Method: {request.method}')
    logger.info(f'Content-Type: {request.content_type}')
    
    # For GET requests (testing endpoint accessibility)
    if request.method == 'GET':
        logger.info('GET request received - endpoint check')
        return jsonify({
            'status': 'success',
            'message': 'Mailgun webhook endpoint is accessible',
            'timestamp': datetime.utcnow().isoformat()
        })

    try:
        # Get the initialized Mailgun service from extensions
        mailgun = MailgunService.get_current_service()
        
        # Verify webhook signature
        if not mailgun.verify_webhook_signature(request):
            logger.error('Invalid webhook signature')
            return jsonify({
                'status': 'error',
                'message': 'Invalid webhook signature'
            }), 401

        # Parse webhook data
        email_data = mailgun.parse_webhook_data(request.form)
        
        logger.info('Parsed Email Data:')
        for key, value in email_data.items():
            value_str = str(value)
            if len(value_str) > 100:
                value_str = value_str[:100] + '...'
            logger.info(f'  {key}: {value_str}')

        # Validate newsletter
        if not mailgun.is_valid_newsletter(email_data):
            logger.warning('Invalid newsletter source')
            return jsonify({
                'status': 'error',
                'message': 'Invalid newsletter source'
            }), 400

        # Get system user
        system_user = get_or_create_system_user()
        
        # Create newsletter entry with retry mechanism
        max_retries = 3
        retry_delay = 1  # seconds
        last_error = None

        for attempt in range(max_retries):
            try:
                newsletter = Newsletter(
                    user_id=system_user.user_id,
                    subject=email_data['subject'],
                    body=email_data.get('body', ''),
                    date_received=email_data['date_received'],
                    topic=classify_newsletter(email_data['subject'], email_data.get('body', '')),
                    summary=extract_summary(email_data.get('body', ''))
                )
                
                db.session.add(newsletter)
                db.session.commit()
                
                logger.info(f'Successfully created newsletter entry with ID: {newsletter.newsletter_id}')
                logger.info(f'Classified topic: {newsletter.topic}')
                logger.info(f'Generated summary length: {len(newsletter.summary)} chars')
                
                return jsonify({
                    'status': 'success',
                    'message': 'Newsletter entry created',
                    'newsletter_id': newsletter.newsletter_id,
                    'topic': newsletter.topic
                })

            except SQLAlchemyError as e:
                last_error = str(e)
                logger.warning(f'Database operation failed on attempt {attempt + 1}: {last_error}')
                db.session.rollback()
                
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                else:
                    logger.error(f'Failed to save newsletter after {max_retries} attempts')
                    raise

    except Exception as e:
        error_msg = f'Error processing webhook: {str(e)}'
        logger.error(error_msg)
        return jsonify({
            'status': 'error',
            'message': error_msg
        }), 500

@webhooks.route('/webhooks/mailgun/test')
def test_webhook():
    """Test endpoint to verify webhook accessibility."""
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        
        return jsonify({
            'status': 'success',
            'message': 'Webhook test endpoint is accessible',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f'Test endpoint error: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500 