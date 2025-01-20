from app import db

from .user import User
from .newsletter import Newsletter
from .digest import Digest

# Define keywords for classification
keywords = {
    "crypto": ["crypto", "bitcoin", "nft"],
    "self_improvement": ["habit", "motivation", "goal"],
    # Add more topics and keywords as needed
}

def classify_newsletter(subject, body):
    """Classify newsletter based on keywords in subject and body."""
    for topic, words in keywords.items():
        if any(word in subject.lower() or word in body.lower() for word in words):
            return topic
    return "unknown"  # Default if no keywords match

__all__ = ['User', 'Newsletter', 'Digest', 'classify_newsletter'] 