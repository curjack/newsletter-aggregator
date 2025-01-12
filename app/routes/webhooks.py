from flask import Blueprint, request, current_app, jsonify
from app.models import Newsletter, db
from app.services.mailgun import MailgunService
from datetime import datetime

webhooks = Blueprint('webhooks', __name__)
mailgun = MailgunService()

@webhooks.route('/webhooks/mailgun', methods=['POST'])
def handle_mailgun_webhook():
    """Handle incoming emails from Mailgun."""
    
    # Log incoming request
    current_app.logger.info("Received Mailgun webhook request")
    current_app.logger.debug(f"Headers: {dict(request.headers)}")
    current_app.logger.debug(f"Form data: {dict(request.form)}")
    
    # Verify webhook signature
    try:
        token = request.form.get('token')
        timestamp = request.form.get('timestamp')
        signature = request.form.get('signature')
        
        current_app.logger.info(f"Verifying signature - Token: {token}, Timestamp: {timestamp}")
        
        if not all([token, timestamp, signature]):
            current_app.logger.error("Missing signature parameters")
            return jsonify({'error': 'Missing signature parameters'}), 400
            
        if not mailgun.verify_webhook_signature(token, timestamp, signature):
            current_app.logger.error("Invalid signature")
            return jsonify({'error': 'Invalid signature'}), 401
            
        current_app.logger.info("Signature verification successful")
    except Exception as e:
        current_app.logger.error(f"Signature verification error: {str(e)}")
        return jsonify({'error': 'Signature verification failed'}), 401

    try:
        # Parse the webhook data
        parsed_data = mailgun.parse_webhook_data(request.form)
        current_app.logger.info(f"Parsed webhook data: {parsed_data}")
        
        # Validate the sender
        if not mailgun.is_valid_newsletter(parsed_data['from_address']):
            current_app.logger.error(f"Invalid newsletter source: {parsed_data['from_address']}")
            return jsonify({'error': 'Invalid newsletter source'}), 400

        # Create new newsletter entry
        newsletter = Newsletter(
            user_id=1,  # This will be updated when user management is implemented
            subject=parsed_data['subject'],
            body=parsed_data['body'],
            topic=parsed_data['topic'],
            date_received=datetime.utcnow(),  # Use current time as fallback
            summary=parsed_data['summary']
        )

        # Save to database
        db.session.add(newsletter)
        db.session.commit()
        
        current_app.logger.info(f"Successfully stored newsletter with ID: {newsletter.newsletter_id}")
        return jsonify({'status': 'success', 'newsletter_id': newsletter.newsletter_id}), 201

    except Exception as e:
        current_app.logger.error(f"Error processing webhook: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

# Add a test endpoint to verify the webhook URL is accessible
@webhooks.route('/webhooks/mailgun/test', methods=['GET'])
def test_webhook():
    """Test endpoint to verify the webhook URL is accessible."""
    return jsonify({
        'status': 'success',
        'message': 'Webhook endpoint is accessible',
        'timestamp': datetime.utcnow().isoformat()
    }) 