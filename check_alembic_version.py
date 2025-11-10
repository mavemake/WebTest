import sqlite3
import os

# Connect to the database
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check alembic version
try:
    cursor.execute("SELECT version_num FROM alembic_version")
    version = cursor.fetchone()
    if version:
        print(f"Alembic version: {version[0]}")
    else:
        print("No alembic version found")
except sqlite3.OperationalError as e:
    print(f"Alembic version table not found: {e}")

conn.close()