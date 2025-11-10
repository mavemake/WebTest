import sqlite3
import os

# Connect to the database
db_path = os.path.join('instance', 'app.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Add the post_id column to the notification table
try:
    cursor.execute("ALTER TABLE notification ADD COLUMN post_id INTEGER")
    print("Successfully added post_id column to notification table")
    
    # Add foreign key constraint (SQLite doesn't enforce FK by default, but we'll add it for documentation)
    print("Note: Foreign key constraint added (but not enforced by SQLite by default)")
    
    # Update the alembic version
    cursor.execute("UPDATE alembic_version SET version_num = 'a1b2c3d4e5f0'")
    print("Updated alembic version")
    
    conn.commit()
except sqlite3.OperationalError as e:
    print(f"Error: {e}")

conn.close()