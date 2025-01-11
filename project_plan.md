PROJECT-PLAN.md
1. Overview
This document serves as the central reference for our Newsletter Aggregation & Summarization MVP. It outlines:

Project Goals & Scope
Tech Stack & Data Model
Implementation Phases & Tasks
Testing & QA
Coding Best Practices & Guidelines
Future Enhancements (Roadmap)
The Cursor (AI Developer) should consult this plan at all times to:

Avoid drifting from the requirements.
Prevent code-related hallucinations (i.e., generating code that contradicts specified logic or best practices).
Maintain consistency and reliability in all code and documentation.

2. Project Goals & MVP Scope
Goals
Aggregate Newsletters in one place, reducing inbox clutter.
Classify & Summarize each newsletter into short snippets grouped by topic.
Send a Single Digest email based on a user-defined schedule (daily/weekly).
MVP Scope
User Registration & Onboarding
Basic Newsletter Ingestion (via forwarding or IMAP/POP integration)
Rule-Based Topic Classification
Simple Summaries (first paragraph or bullet points)
Digest Generation & Delivery (daily/weekly email)
Minimal UI for User Settings (frequency, topics, etc.)

3. Tech Stack & Data Model
Tech Stack
Backend: Node.js/Express or Python/Flask (to be confirmed in final decision)
Database: PostgreSQL or MySQL (PostgreSQL is recommended)
Email Services:
Inbound: Mailgun/SendGrid Inbound Parse or IMAP fetch
Outbound: SendGrid/Mailgun/AWS SES
Scheduling: Cron-like job (Node Cron, Celery, or equivalent)
Optional Frontend: Minimal HTML/CSS/JS or a lightweight React/Vue setup for user dashboards
Data Model
Users Table

user_id (PK)
email (unique)
password_hash
settings (JSON or columns for digest frequency, time preference, etc.)
Newsletters Table

newsletter_id (PK)
user_id (FK → Users)
topic (string)
subject (string)
body (text)
date_received (timestamp)
summary (text)
Digests Table

digest_id (PK)
user_id (FK → Users)
date_sent (timestamp)
content (text or JSON with grouped newsletter data)

4. Implementation Phases & Tasks
The project will be built in four main phases:

Phase 1: Setup & Infrastructure
Create project with minimal web server & DB connection.
Set up the schema above.
Configure environment variables (DB credentials, email service credentials).

Phase 2: Newsletter Ingestion & Classification
Inbound Emails: Implement logic to capture incoming emails (Mailgun/SendGrid or IMAP).
Store each newsletter (subject, body, date_received) in the database.
Classify using a rule-based approach (keywords → topic).

Phase 3: Summaries & Digest Delivery
Generate Summaries: Extract the first paragraph or bullet points.
Scheduler: Use cron or similar to trigger digest compilation daily or weekly.
Digest Compilation: Group newsletters by topic, compile them into a single email body.
Send Email: Deliver the digest to the user via an outbound email service.
Phase 4: Testing & Deployment

Automated Tests: Unit tests for parsing, classification, digest generation.
Manual QA: Check email rendering in various clients (Gmail, Outlook, etc.).
Deployment: Push to production environment, ensure environment variables are securely set.

5. Testing & QA
Unit Tests

Verify that newsletters are stored correctly.
Test classification logic with sample subjects/bodies.
Test summary extraction (e.g., bullet points, first paragraph).
Validate digest creation & email sending.
Integration Tests

Simulate end-to-end flow (inbound email → DB → classification → scheduled digest).
Manual Testing

Confirm email formatting on Gmail, Outlook, mobile devices.
Confirm scheduling triggers at correct times (time zones, user preferences).

6. Coding Best Practices & Guidelines
Use a Modular Architecture

Separate business logic, data access, and utility functions.
Keep code organized in meaningful modules (e.g., /models, /controllers, /services).
Follow Clean Code Principles

Use descriptive function names and clear variable naming.
Avoid large, monolithic functions—split complex logic into smaller, testable functions.
Error Handling

Always handle potential exceptions with try/catch or language-specific methods.
Log errors with sufficient details (never expose sensitive info).
Security & Data Privacy

Encrypt passwords (BCrypt or equivalent).
Validate email addresses before saving.
Ensure HTTPS for all communication.
Store API keys and credentials in environment variables, never commit to source control.
Avoid Hallucinations (AI-Specific)

Only generate code requested by this document or the human in charge.
If uncertain about requirements, prompt the human for clarification.
No guesswork—reference explicit instructions from this project plan.
Testing Coverage

Aim for 80%+ coverage on critical modules (classification, summarization, scheduling).
Use coverage tools (e.g., Jest, Coverage.py, etc.).
Documentation & Comments

In each module or function, add docstrings or comments explaining the logic.
Keep a brief CHANGELOG of major updates.

7. Future Enhancements (Roadmap)

After the MVP is stable, we can consider the following upgrades:

Advanced Summarization (GPT-based or specialized NLP)
CTA & Link Extraction
Personalization & Priority (feedback loops, user preferences)
Vacation Mode & Dynamic Scheduling
Archive & Search (User can search past newsletters)
Multi-Platform Integration (Slack/Telegram bots)
Analytics & Insights (reading stats, open rates)
Monetization & Partnerships (freemium models, affiliates)

8. Conclusion
This Project-Plan.md is the source of truth for the MVP. Cursor (AI Developer) must adhere to the outlined phases, data models, best practices, and guidelines here. If the agent encounters uncertainty or requires a decision that is not covered in this document, it should prompt the human for clarification before proceeding.

By following these steps and maintaining best practices, we will deliver a robust, secure, and user-friendly newsletter aggregator that meets the initial MVP requirements and lays a strong foundation for future enhancements.