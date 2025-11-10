import sqlite3
import os

# Connect to the database
db_path = os.path.join('instance', 'app.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get table info
cursor.execute("PRAGMA table_info(notification)")
columns = cursor.fetchall()

print("Notification table columns:")
for col in columns:
    print(col)

conn.close()