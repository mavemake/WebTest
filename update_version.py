import sqlite3
import os

# Connect to the database
db_path = os.path.join('instance', 'app.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Update the alembic version
cursor.execute("UPDATE alembic_version SET version_num = 'a1b2c3d4e5f0'")
conn.commit()
print("Alembic version updated")

conn.close()