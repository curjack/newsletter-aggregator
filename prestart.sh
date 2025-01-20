#!/bin/bash
set -e

echo "Waiting for database..."
python -c "
import time
import os
import sys
from sqlalchemy import create_engine

def wait_for_db(url, max_retries=5, retry_delay=5):
    print(f'Checking database connection (max {max_retries} attempts)...')
    for attempt in range(max_retries):
        try:
            print(f'Attempt {attempt + 1} of {max_retries}...')
            engine = create_engine(url)
            with engine.connect() as conn:
                conn.execute('SELECT 1')
            print('Database connection successful!')
            return True
        except Exception as e:
            print(f'Attempt {attempt + 1} failed: {str(e)}')
            if attempt < max_retries - 1:
                print(f'Retrying in {retry_delay} seconds...')
                time.sleep(retry_delay)
            else:
                print('All database connection attempts failed')
                return False

db_url = os.environ.get('DATABASE_URL', '')
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)

if not wait_for_db(db_url):
    sys.exit(1)
"

echo "Running database migrations..."
FLASK_APP=app flask db upgrade

echo "Verifying database setup..."
python -c "
from app import create_app, db
from sqlalchemy import text

app = create_app('production')
with app.app_context():
    with db.engine.connect() as conn:
        tables = conn.execute(text('SELECT tablename FROM pg_tables WHERE schemaname = current_schema()')).fetchall()
        print(f'Current tables: {[table[0] for table in tables]}')" 