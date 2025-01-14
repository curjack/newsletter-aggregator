from flask import Blueprint, request, jsonify, current_app
import logging
from datetime import datetime
from app import db
from app.models.newsletter import Newsletter

webhooks = Blueprint('webhooks', __name__)
logger = logging.getLogger(__name__)

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

    # For POST requests (actual webhooks)
    logger.info('Headers:')
    for header, value in request.headers.items():
        logger.info(f'  {header}: {value}')
    
    logger.info('Form Data:')
    for key, value in request.form.items():
        # Truncate long values for logging
        value_str = str(value)
        if len(value_str) > 100:
            value_str = value_str[:100] + '...'
        logger.info(f'  {key}: {value_str}')

    try:
        # Extract email data
        email_data = {
            'sender': request.form.get('sender'),
            'recipient': request.form.get('recipient'),
            'subject': request.form.get('subject'),
            'body_plain': request.form.get('body-plain'),
            'stripped_text': request.form.get('stripped-text'),
            'timestamp': request.form.get('timestamp')
        }
        
        logger.info('Parsed Email Data:')
        for key, value in email_data.items():
            value_str = str(value)
            if len(value_str) > 100:
                value_str = value_str[:100] + '...'
            logger.info(f'  {key}: {value_str}')

        # Create newsletter entry
        newsletter = Newsletter(
            user_id=1,  # TODO: Implement user lookup based on recipient
            subject=email_data['subject'],
            body=email_data['stripped_text'] or email_data['body_plain'],
            date_received=datetime.utcnow(),
            topic='Uncategorized'  # TODO: Implement topic extraction
        )
        
        db.session.add(newsletter)
        db.session.commit()
        
        logger.info(f'Successfully created newsletter entry with ID: {newsletter.newsletter_id}')
        
        return jsonify({
            'status': 'success',
            'message': 'Newsletter processed successfully',
            'newsletter_id': newsletter.newsletter_id
        }), 200
        
    except Exception as e:
        logger.error(f'Error processing webhook: {str(e)}', exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f'Error processing webhook: {str(e)}'
        }), 500

@webhooks.route('/webhooks/mailgun/test')
def test_webhook():
    """Test endpoint to verify webhook accessibility."""
    logger.info('Test endpoint accessed')
    return jsonify({
        'status': 'success',
        'message': 'Webhook test endpoint is accessible',
        'timestamp': datetime.utcnow().isoformat()
    }) 