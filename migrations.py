import os
import sys
from flask import Flask
from flask_migrate import Migrate, init, migrate, upgrade
from sqlalchemy import text

def run_migrations():
    try:
        print('Setting up Flask application...')
        from app import create_app, db
        
        app = create_app('production')
        
        with app.app_context():
            print('Checking migrations directory...')
            if not os.path.exists('migrations'):
                print('Initializing migrations directory...')
                init()
            
            print('Generating migrations...')
            migrate(message='initial migration')
            
            print('Applying migrations...')
            upgrade()
            
            print('Verifying database tables...')
            with db.engine.connect() as conn:
                tables = conn.execute(text('SELECT tablename FROM pg_tables WHERE schemaname = current_schema()')).fetchall()
                print(f'Current tables: {[table[0] for table in tables]}')
            
            print('Database setup completed successfully!')
            return True
            
    except Exception as e:
        print(f'Error during database setup: {str(e)}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = run_migrations()
    sys.exit(0 if success else 1) 