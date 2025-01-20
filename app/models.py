# Define keywords for classification
keywords = {
    "crypto": ["crypto", "bitcoin", "nft"],
    "self_improvement": ["habit", "motivation", "goal"],
    # Add more topics and keywords as needed
}

# Function to classify newsletter topic
def classify_newsletter(subject, body):
    for topic, words in keywords.items():
        if any(word in subject.lower() or word in body.lower() for word in words):
            return topic
    return "unknown"  # Default if no keywords match

# Example usage in newsletter processing
# newsletter.topic = classify_newsletter(newsletter.subject, newsletter.body)
# db.session.commit() 