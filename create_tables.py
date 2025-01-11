from app import app, db

def create_tables():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("All tables created successfully!")

if __name__ == "__main__":
    create_tables() 