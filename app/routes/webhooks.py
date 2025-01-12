from flask import Blueprint, request, current_app, jsonify
import logging
from app import db
from app.models import Newsletter
from app.services.mailgun import MailgunService
from datetime import datetime

webhooks = Blueprint('webhooks', __name__)
mailgun = MailgunService()

@webhooks.route('/webhooks/mailgun', methods=['POST'])
def handle_mailgun_webhook():
    current_app.logger.info('Received Mailgun webhook request')
    current_app.logger.debug(f'Headers: {dict(request.headers)}')
    current_app.logger.debug(f'Form data: {dict(request.form)}')
    
    try:
        # Verify webhook signature
        if not mailgun.verify_webhook_signature(request):
            current_app.logger.warning('Invalid webhook signature')
            return jsonify({'error': 'Invalid signature'}), 401

        # Parse webhook data
        data = mailgun.parse_webhook_data(request.form)
        current_app.logger.info(f'Parsed webhook data: {data}')
        
        # Validate newsletter source
        if not mailgun.is_valid_newsletter(data):
            current_app.logger.warning(f'Invalid newsletter source: {data.get("from_address")}')
            return jsonify({'error': 'Invalid newsletter source'}), 400

        # Create newsletter entry
        newsletter = Newsletter(
            user_id=1,  # TODO: Update with actual user management
            subject=data['subject'],
            body=data['body'],
            topic=data.get('topic', ''),
            date_received=data['date_received']
        )
        
        db.session.add(newsletter)
        db.session.commit()
        
        current_app.logger.info(f'Successfully created newsletter entry: {newsletter.newsletter_id}')
        return jsonify({'status': 'success', 'newsletter_id': newsletter.newsletter_id}), 201
        
    except Exception as e:
        current_app.logger.error(f'Error processing webhook: {str(e)}', exc_info=True)
        return jsonify({'error': str(e)}), 500

@webhooks.route('/webhooks/mailgun/test', methods=['GET'])
def test_webhook():
    return jsonify({
        'status': 'success',
        'message': 'Webhook endpoint is accessible',
        'timestamp': str(datetime.utcnow())
    }) 