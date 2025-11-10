import sqlite3
import os

# Check if database exists
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
print('Database exists:', os.path.exists(db_path))

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tables in database:')
for table in tables:
    print(table[0])

conn.close()