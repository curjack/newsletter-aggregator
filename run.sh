#!/bin/bash

# Initialize database
python -c "
from app import create_app, db
app = create_app('production')
with app.app_context():
    db.create_all()
"

# Start Gunicorn
exec gunicorn wsgi:app 