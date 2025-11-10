import sqlite3
import os

# Connect to the database
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Update alembic version to the latest migration
current_version = '34f65c0a92e1'  # This should match the revision ID of our latest migration
cursor.execute("UPDATE alembic_version SET version_num = ?", (current_version,))

# Commit and close
conn.commit()
conn.close()

print(f"Alembic version updated to {current_version}")