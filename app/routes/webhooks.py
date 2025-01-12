from flask import Blueprint, request, current_app, jsonify, make_response
import logging
from app import db
from app.models import Newsletter
from app.services.mailgun import MailgunService
from datetime import datetime

webhooks = Blueprint('webhooks', __name__)
mailgun = MailgunService()

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response

@webhooks.route('/webhooks/mailgun', methods=['POST', 'GET', 'OPTIONS'])
def handle_mailgun_webhook():
    current_app.logger.info('==========================================')
    current_app.logger.info('Received request to webhook endpoint')
    current_app.logger.info(f'Method: {request.method}')
    current_app.logger.info(f'Content-Type: {request.content_type}')
    
    # Handle OPTIONS request for CORS
    if request.method == 'OPTIONS':
        response = make_response()
        return add_cors_headers(response)
    
    # For GET requests, return a simple test response
    if request.method == 'GET':
        response = jsonify({
            'status': 'success',
            'message': 'Webhook endpoint is accessible via GET',
            'timestamp': str(datetime.utcnow())
        })
        return add_cors_headers(response)
    
    # Continue with POST handling
    current_app.logger.info('Headers:')
    for header, value in request.headers.items():
        current_app.logger.info(f'  {header}: {value}')
    
    # Log all available request data
    current_app.logger.info('Form Data:')
    for key, value in request.form.items():
        current_app.logger.info(f'  {key}: {value}')
    
    current_app.logger.info('Query String:')
    for key, value in request.args.items():
        current_app.logger.info(f'  {key}: {value}')
    
    current_app.logger.info('Raw Data:')
    current_app.logger.info(request.get_data(as_text=True))
    current_app.logger.info('==========================================')
    
    try:
        # Verify webhook signature
        if not mailgun.verify_webhook_signature(request):
            current_app.logger.warning('Invalid webhook signature')
            response = jsonify({'error': 'Invalid signature'}), 401
            return add_cors_headers(response[0]), response[1]

        # Parse webhook data
        data = mailgun.parse_webhook_data(request.form)
        current_app.logger.info('Parsed webhook data:')
        for key, value in data.items():
            current_app.logger.info(f'  {key}: {value}')
        
        # Validate newsletter source
        if not mailgun.is_valid_newsletter(data):
            current_app.logger.warning(f'Invalid newsletter source: {data.get("from_address")}')
            response = jsonify({'error': 'Invalid newsletter source'}), 400
            return add_cors_headers(response[0]), response[1]

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
        response = jsonify({'status': 'success', 'newsletter_id': newsletter.newsletter_id}), 201
        return add_cors_headers(response[0]), response[1]
        
    except Exception as e:
        current_app.logger.error(f'Error processing webhook: {str(e)}', exc_info=True)
        response = jsonify({'error': str(e)}), 500
        return add_cors_headers(response[0]), response[1]

@webhooks.route('/webhooks/mailgun/test', methods=['GET'])
def test_webhook():
    current_app.logger.info('Test endpoint accessed')
    response = jsonify({
        'status': 'success',
        'message': 'Webhook endpoint is accessible',
        'timestamp': str(datetime.utcnow())
    })
    return add_cors_headers(response) 