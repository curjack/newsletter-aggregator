from app import create_app, db

app = create_app('production')

# Initialize database tables
with app.app_context():
    db.create_all() 