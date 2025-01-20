Infrastructure Overview
Project Structure:
app/: Main application code.
models.py: Contains database models and classification function.
routes/: Handles API endpoints, including webhooks.
services/: Integrates external services like Mailgun.
__init__.py: Initializes the Flask app and its extensions.
migrations/: Database migration scripts.
templates/: HTML templates (if applicable).
static/: Static files like CSS and JavaScript (if applicable).
Configuration:
config.py: Manages application configuration, including database URLs.
.env: Environment variables for local development.
Deployment:
render.yaml: Configures deployment on Render, including build and start commands.
4. Database:
PostgreSQL database hosted on Render.
Tables: users, newsletters, digests.
5. External Services:
Mailgun for receiving emails via webhooks.
Current Features
Email Reception: Handles incoming emails via Mailgun webhooks.
Newsletter Storage: Stores parsed email data in the newsletters table.
Classification: Classifies newsletters based on keywords in the subject and body.
System User: Uses a default system user for associating newsletters.