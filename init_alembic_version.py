import sqlite3
import os

# Connect to the database
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create alembic_version table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS alembic_version (
    version_num VARCHAR(32) NOT NULL,
    PRIMARY KEY (version_num)
)
''')

# Insert the current version (the latest migration we created)
current_version = '34f65c0a92e1'  # This should match the revision ID of our latest migration
cursor.execute("DELETE FROM alembic_version")  # Clear any existing version
cursor.execute("INSERT INTO alembic_version (version_num) VALUES (?)", (current_version,))

# Commit and close
conn.commit()
conn.close()

print(f"Alembic version initialized to {current_version}")