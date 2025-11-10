import sqlite3
import os

# Connect to the database
db_path = os.path.join('instance', 'app.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create post_share table
cursor.execute('''
CREATE TABLE IF NOT EXISTS post_share (
    id INTEGER PRIMARY KEY,
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    shared_at DATETIME NOT NULL,
    share_content TEXT,
    FOREIGN KEY (post_id) REFERENCES post (id),
    FOREIGN KEY (user_id) REFERENCES user (id)
)
''')

# Create comment_reaction table
cursor.execute('''
CREATE TABLE IF NOT EXISTS comment_reaction (
    id INTEGER PRIMARY KEY,
    comment_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    reaction_type VARCHAR(20) NOT NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (comment_id) REFERENCES comment (id),
    FOREIGN KEY (user_id) REFERENCES user (id)
)
''')

# Create friendship table
cursor.execute('''
CREATE TABLE IF NOT EXISTS friendship (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    friend_id INTEGER NOT NULL,
    status VARCHAR(20),
    created_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (friend_id) REFERENCES user (id)
)
''')

# Commit changes and close connection
conn.commit()
print("Tables created successfully!")
conn.close()