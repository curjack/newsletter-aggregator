import hmac
import hashlib
from datetime import datetime
from flask import current_app

class MailgunService:
    def __init__(self, app=None):
        self.app = app
        self.api_key = None
        self.webhook_signing_key = None
        self.domain = None
        
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # Store configuration
        self.api_key = app.config.get('MAILGUN_API_KEY')
        self.webhook_signing_key = app.config.get('MAILGUN_WEBHOOK_SIGNING_KEY')
        self.domain = app.config.get('MAILGUN_DOMAIN')
        
        # Register to app extensions
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['mailgun'] = self

        # Log only if logger is configured
        if app.logger:
            app.logger.info('Mailgun service initialized')
            app.logger.debug(f'Domain: {self.domain}')

    @staticmethod
    def get_current_service():
        """Get the current Mailgun service instance."""
        if not hasattr(current_app, 'extensions') or 'mailgun' not in current_app.extensions:
            raise RuntimeError("Mailgun service not initialized. Did you forget to call init_app()?")
        return current_app.extensions['mailgun']

    def verify_webhook_signature(self, request):
        """Verify that the webhook request came from Mailgun."""
        try:
            timestamp = request.form.get('timestamp')
            token = request.form.get('token')
            signature = request.form.get('signature')

            current_app.logger.debug('Verifying webhook signature')
            current_app.logger.debug(f'Timestamp: {timestamp}')
            current_app.logger.debug(f'Token: {token}')
            current_app.logger.debug(f'Signature: {signature}')

            if not all([timestamp, token, signature]):
                current_app.logger.warning('Missing signature parameters')
                return False

            hmac_digest = hmac.new(
                key=self.webhook_signing_key.encode('utf-8'),
                msg=f'{timestamp}{token}'.encode('utf-8'),
                digestmod=hashlib.sha256
            ).hexdigest()

            current_app.logger.debug(f'Computed signature: {hmac_digest}')
            return hmac.compare_digest(signature, hmac_digest)
        except Exception as e:
            current_app.logger.error(f'Error verifying webhook signature: {str(e)}')
            return False

    def parse_webhook_data(self, form_data):
        """Parse the webhook data from Mailgun."""
        try:
            current_app.logger.debug('Parsing webhook data')
            return {
                'from_address': form_data.get('sender'),
                'subject': form_data.get('subject'),
                'body': form_data.get('body-plain'),  # or 'stripped-text' depending on Mailgun's config
                'date_received': datetime.utcnow(),
                'recipient': form_data.get('recipient'),
                'message_id': form_data.get('Message-Id')
            }
        except Exception as e:
            current_app.logger.error(f'Error parsing webhook data: {str(e)}')
            raise

    def is_valid_newsletter(self, data):
        """Validate if the email is from an allowed newsletter source."""
        # For testing, accept all emails
        current_app.logger.debug(f'Validating newsletter from: {data.get("from_address")}')
        return True 