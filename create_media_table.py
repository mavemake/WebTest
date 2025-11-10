import sqlite3
import os

# Connect to the database
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the media table
cursor.execute('''
CREATE TABLE IF NOT EXISTS media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    media_type TEXT NOT NULL,
    post_id INTEGER,
    comment_id INTEGER,
    date_uploaded DATETIME NOT NULL,
    FOREIGN KEY (post_id) REFERENCES post (id),
    FOREIGN KEY (comment_id) REFERENCES comment (id)
)
''')

# Commit and close
conn.commit()
conn.close()

print("Media table created successfully!")