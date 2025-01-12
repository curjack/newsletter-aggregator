from flask import Blueprint, request, current_app, jsonify
import logging
from app import db
from app.models import Newsletter
from app.services.mailgun import MailgunService
from datetime import datetime

webhooks = Blueprint('webhooks', __name__)
mailgun = MailgunService()

@webhooks.route('/webhooks/mailgun', methods=['POST', 'GET'])
def handle_mailgun_webhook():
    current_app.logger.info('==========================================')
    current_app.logger.info('Received request to webhook endpoint')
    current_app.logger.info(f'Method: {request.method}')
    current_app.logger.info(f'Content-Type: {request.content_type}')
    
    # For GET requests, return a simple test response
    if request.method == 'GET':
        return jsonify({
            'status': 'success',
            'message': 'Webhook endpoint is accessible via GET',
            'timestamp': str(datetime.utcnow())
        })
    
    # Continue with POST handling
    current_app.logger.info('Headers:')
    for header, value in request.headers.items():
        current_app.logger.info(f'  {header}: {value}')
    current_app.logger.info('Form Data:')
    for key, value in request.form.items():
        current_app.logger.info(f'  {key}: {value}')
    current_app.logger.info('Raw Data:')
    current_app.logger.info(request.get_data(as_text=True))
    current_app.logger.info('==========================================')
    
    try:
        # Verify webhook signature
        if not mailgun.verify_webhook_signature(request):
            current_app.logger.warning('Invalid webhook signature')
            return jsonify({'error': 'Invalid signature'}), 401

        # Parse webhook data
        data = mailgun.parse_webhook_data(request.form)
        current_app.logger.info('Parsed webhook data:')
        for key, value in data.items():
            current_app.logger.info(f'  {key}: {value}')
        
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
    current_app.logger.info('Test endpoint accessed')
    return jsonify({
        'status': 'success',
        'message': 'Webhook endpoint is accessible',
        'timestamp': str(datetime.utcnow())
    }) 