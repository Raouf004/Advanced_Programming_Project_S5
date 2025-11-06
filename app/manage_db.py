import sys
from app.database import init_db, drop_db, engine
from sqlalchemy import text

def create_database():
    """Create all tables"""
    print("Creating database tables...")
    init_db()

def reset_database():
    """Drop and recreate all tables"""
    response = input("Are you sure you want to reset the database? This will delete all data! (yes/no): ")
    if response.lower() == 'yes':
        print("Dropping all tables...")
        drop_db()
        print("Creating tables...")
        init_db()
        print("Database reset complete!")
    else:
        print("Operation cancelled.")

def check_connection():
    """Check database connection"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✓ Database connection successful!")
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def show_tables():
    """Show all tables in database"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            tables = result.fetchall()
            if tables:
                print("\nTables in database:")
                for table in tables:
                    print(f"  - {table[0]}")
            else:
                print("No tables found in database.")
    except Exception as e:
        print(f"Error fetching tables: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python manage_db.py [command]")
        print("Commands:")
        print("  create    - Create database tables")
        print("  reset     - Drop and recreate all tables")
        print("  check     - Check database connection")
        print("  tables    - Show all tables")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "create":
        create_database()
    elif command == "reset":
        reset_database()
    elif command == "check":
        check_connection()
    elif command == "tables":
        show_tables()
    else:
        print(f"Unknown command: {command}")