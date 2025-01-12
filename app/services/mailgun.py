import hmac
import hashlib
from typing import Dict, Any
import requests
from flask import current_app

class MailgunService:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.api_key = app.config['MAILGUN_API_KEY']
        self.domain = app.config['MAILGUN_DOMAIN']
        self.base_url = app.config['MAILGUN_BASE_URL']
        self.webhook_signing_key = app.config['MAILGUN_WEBHOOK_SIGNING_KEY']

    def verify_webhook_signature(self, token: str, timestamp: str, signature: str) -> bool:
        """Verify that the webhook request came from Mailgun."""
        hmac_digest = hmac.new(
            key=self.webhook_signing_key.encode('utf-8'),
            msg=f'{timestamp}{token}'.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, hmac_digest)

    def parse_webhook_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse the webhook data into a format suitable for our Newsletter model."""
        return {
            'subject': data.get('subject', ''),
            'body': data.get('body-plain', ''),  # We'll store the plain text version
            'from_address': data.get('sender', ''),
            'date_received': data.get('Date', ''),
            'topic': data.get('subject', '').split(':')[0].strip(),  # Basic topic extraction
            'summary': ''  # This will be populated by a summarization service later
        }

    def is_valid_newsletter(self, from_address: str) -> bool:
        """
        Validate if the email is from a legitimate newsletter source.
        This can be expanded based on your requirements.
        """
        # Add your newsletter validation logic here
        # For example, check against a whitelist of domains or email addresses
        return True  # For now, accept all emails 