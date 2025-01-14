import click
from flask.cli import with_appcontext
from . import db

def register_commands(app):
    """Register Flask CLI commands."""
    
    @app.cli.command('init-db')
    @with_appcontext
    def init_db():
        """Initialize the database."""
        db.create_all()
        click.echo('Initialized the database.')
    
    @app.cli.command('drop-db')
    @with_appcontext
    def drop_db():
        """Drop all database tables."""
        if click.confirm('Are you sure you want to drop all tables?'):
            db.drop_all()
            click.echo('Dropped all tables.')
    
    @app.cli.command('reset-db')
    @with_appcontext
    def reset_db():
        """Reset the database (drop all tables and recreate)."""
        if click.confirm('Are you sure you want to reset the database?'):
            db.drop_all()
            db.create_all()
            click.echo('Database has been reset.')
    
    @app.cli.command('check-db')
    @with_appcontext
    def check_db():
        """Check database connection and print table information."""
        try:
            # Check connection
            db.session.execute('SELECT 1')
            click.echo('Database connection: OK')
            
            # Get table information
            tables = db.engine.table_names()
            click.echo(f'\nDatabase tables ({len(tables)}):')
            for table in tables:
                click.echo(f'  - {table}')
                
        except Exception as e:
            click.echo(f'Database error: {str(e)}', err=True) 