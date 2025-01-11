from app import app, db
from sqlalchemy import inspect

def check_schema():
    inspector = inspect(db.engine)
    
    print("\nDatabase Schema:")
    print("=" * 50)
    
    for table_name in inspector.get_table_names():
        print(f"\nTable: {table_name}")
        print("-" * 30)
        
        # Get columns
        columns = inspector.get_columns(table_name)
        print("Columns:")
        for column in columns:
            nullable = "NULL" if column['nullable'] else "NOT NULL"
            print(f"  - {column['name']}: {column['type']} {nullable}")
        
        # Get foreign keys
        foreign_keys = inspector.get_foreign_keys(table_name)
        if foreign_keys:
            print("\nForeign Keys:")
            for fk in foreign_keys:
                print(f"  - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
        
        # Get indexes
        indexes = inspector.get_indexes(table_name)
        if indexes:
            print("\nIndexes:")
            for idx in indexes:
                unique = "UNIQUE " if idx['unique'] else ""
                print(f"  - {unique}Index on {idx['column_names']}")

if __name__ == "__main__":
    with app.app_context():
        check_schema() 