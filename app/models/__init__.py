import re
from app import db

from .user import User
from .newsletter import Newsletter
from .digest import Digest

# Define keywords for classification
keywords = {
    "crypto": ["crypto", "bitcoin", "nft"],
    "self_improvement": ["habit", "motivation", "goal"],
    "health": ["health", "fitness", "exercise", "nutrition"],
    "finance": ["finance", "investment", "stock", "market"],
    "tech": ["tech", "ai", "machine learning", "data science"],
    "politics": ["politics", "government", "policy", "elections"],
    "science": ["science", "research", "discovery", "innovation"],
    "entertainment": ["entertainment", "movies", "music", "books"],
    "sports": ["sports", "football", "basketball", "tennis"],
    "travel": ["travel", "vacation", "destination", "adventure"],
    "education": ["education", "school", "learning", "academics"],
    "environment": ["environment", "climate", "sustainability", "eco-friendly"],
    "art": ["art", "painting", "sculpture", "music"],
    "gaming": ["gaming", "video games", "console", "pc"],
    "fashion": ["fashion", "style", "designer", "fashion week"],
    "food": ["food", "cooking", "recipe", "restaurant"],
    "pets": ["pets", "dog", "cat", "animal"],
    "religion": ["religion", "faith", "spirituality", "religion"],
    "other": ["other", "uncategorized", "miscellaneous", "random"],
    # Add more topics and keywords as needed
}

def classify_newsletter(subject, body):
    """Classify newsletter based on keywords in subject and body."""
    for topic, words in keywords.items():
        if any(word in subject.lower() or word in body.lower() for word in words):
            return topic
    return "unknown"  # Default if no keywords match

def extract_summary(body_text: str, max_length: int = 500) -> str:
    """Extract a summary from newsletter body text.
    
    Args:
        body_text (str): The full body text of the newsletter
        max_length (int): Maximum length of the summary
        
    Returns:
        str: Extracted summary, truncated to max_length if necessary
    """
    # Strip HTML if present
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(body_text, 'html.parser')
        text = soup.get_text()
    except ImportError:
        text = body_text
    
    # Split into paragraphs (using double newline)
    paragraphs = text.split('\n\n')
    
    # Initialize variables
    summary = ""
    bullet_pattern = r'^\s*[-*•]|\d+\.|[a-zA-Z]\.'
    
    # Try to find first real paragraph (non-empty, longer than 100 chars)
    for para in paragraphs:
        para = para.strip()
        if para and len(para) >= 100:
            summary = para
            break
    
    # If no good paragraph found, look for bullet points
    if not summary:
        bullet_points = []
        for para in paragraphs:
            lines = para.strip().split('\n')
            if any(re.match(bullet_pattern, line.strip()) for line in lines):
                bullet_points.extend(line.strip() for line in lines 
                                   if re.match(bullet_pattern, line.strip()))
                if bullet_points:
                    summary = '\n'.join(bullet_points[:3])  # Take first 3 bullet points
                    break
    
    # If still no summary, take first non-empty paragraph
    if not summary:
        for para in paragraphs:
            para = para.strip()
            if para:
                summary = para
                break
    
    # Truncate if necessary and add ellipsis
    if len(summary) > max_length:
        summary = summary[:max_length-3] + '...'
    
    return summary

__all__ = ['User', 'Newsletter', 'Digest', 'classify_newsletter', 'extract_summary'] 