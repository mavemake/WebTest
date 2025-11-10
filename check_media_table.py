import sqlite3
import os

# Connect to the database
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if media table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='media'")
result = cursor.fetchone()

if result:
    print("Media table exists!")
else:
    print("Media table does not exist!")

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("All tables:")
for table in tables:
    print(f"  {table[0]}")

conn.close()