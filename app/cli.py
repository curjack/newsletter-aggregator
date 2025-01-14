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