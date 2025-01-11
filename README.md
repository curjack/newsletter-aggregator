# Newsletter Aggregator

A Flask-based newsletter aggregation and summarization service.

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
- Copy `.env.example` to `.env`
- Update the `DATABASE_URL` with your PostgreSQL connection string
- Update other environment variables as needed

4. Initialize the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. Run the application:
```bash
python app.py
```

The server will start at `http://localhost:5000`

## Database Schema

The application uses PostgreSQL with the following main tables:

- Users: Stores user information and preferences
- Newsletters: Stores incoming newsletters with their content and classification
- Digests: Stores compiled newsletter digests sent to users

## Development

- Use `flask db migrate` to generate new migrations after model changes
- Use `flask db upgrade` to apply migrations
- Use `flask db downgrade` to reverse migrations 