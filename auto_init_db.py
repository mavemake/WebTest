"""
Automatic Database Initialization Script

This script will automatically create all required database tables
when the application starts in a deployment environment.
"""
import os
import sys

def init_db_if_needed():
    """Initialize database if it doesn't exist or is missing tables"""
    db_path = os.path.join(os.path.dirname(__file__), 'app.db')
    
    # Check if database exists
    if not os.path.exists(db_path):
        print("Database file not found. Initializing database...")
        try:
            # Import and run the initialization script
            from init_database import initialize_database
            initialize_database()
            print("Database initialized successfully!")
            return True
        except Exception as e:
            print(f"Error initializing database: {e}")
            return False
    else:
        print("Database file exists. Checking tables...")
        # Check if required tables exist
        try:
            import sqlite3
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check for essential tables
            required_tables = ['user', 'post', 'comment']
            missing_tables = []
            
            for table in required_tables:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
                if not cursor.fetchone():
                    missing_tables.append(table)
            
            conn.close()
            
            if missing_tables:
                print(f"Missing tables: {', '.join(missing_tables)}. Initializing database...")
                from init_database import initialize_database
                initialize_database()
                print("Database initialized successfully!")
                return True
            else:
                print("All required tables exist.")
                return True
                
        except Exception as e:
            print(f"Error checking database: {e}")
            return False

if __name__ == "__main__":
    init_db_if_needed()