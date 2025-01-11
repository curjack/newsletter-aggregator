from app import app, db

def drop_tables():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        print("All tables dropped successfully!")

if __name__ == "__main__":
    drop_tables() 