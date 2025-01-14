#!/bin/bash

# Wait for a moment to ensure environment variables are loaded
sleep 5

# Initialize the database
python -c "
from app import create_app, db
app = create_app('production')
with app.app_context():
    db.create_all()
"

# Start Gunicorn
exec gunicorn 'app:create_app()' 