"""
Database Initialization Script

This script can be used to initialize the database with all required tables
if they are missing. Run this script if you encounter database errors.
"""

import sqlite3
import os
from datetime import datetime

def initialize_database():
    """Initialize the database with all required tables"""
    # Connect to the database
    db_path = os.path.join(os.path.dirname(__file__), 'app.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create all the missing tables
    tables_to_create = [
        '''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(20) NOT NULL UNIQUE,
            email VARCHAR(120) NOT NULL UNIQUE,
            image_file VARCHAR(20) NOT NULL,
            profile_image VARCHAR(100),
            password VARCHAR(60) NOT NULL,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            location VARCHAR(100),
            bio TEXT,
            children_count INTEGER DEFAULT 0,
            partners_count INTEGER DEFAULT 0,
            date_joined DATETIME NOT NULL
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS post (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(100),
            content TEXT NOT NULL,
            date_posted DATETIME NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS comment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            date_posted DATETIME NOT NULL,
            user_id INTEGER NOT NULL,
            post_id INTEGER NOT NULL,
            parent_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES user (id),
            FOREIGN KEY (post_id) REFERENCES post (id),
            FOREIGN KEY (parent_id) REFERENCES comment (id)
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS message (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            sender_id INTEGER NOT NULL,
            recipient_id INTEGER NOT NULL,
            is_read BOOLEAN,
            FOREIGN KEY (sender_id) REFERENCES user (id),
            FOREIGN KEY (recipient_id) REFERENCES user (id)
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS notification (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            user_id INTEGER NOT NULL,
            is_read BOOLEAN,
            notification_type VARCHAR(50) NOT NULL,
            post_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES user (id),
            FOREIGN KEY (post_id) REFERENCES post (id)
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS post_like (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            post_id INTEGER NOT NULL,
            date_liked DATETIME NOT NULL,
            UNIQUE(user_id, post_id),
            FOREIGN KEY (user_id) REFERENCES user (id),
            FOREIGN KEY (post_id) REFERENCES post (id)
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS post_share (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            shared_at DATETIME NOT NULL,
            share_content TEXT,
            FOREIGN KEY (post_id) REFERENCES post (id),
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS comment_reaction (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comment_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            reaction_type VARCHAR(20) NOT NULL,
            reacted_at DATETIME NOT NULL,
            UNIQUE(comment_id, user_id, reaction_type),
            FOREIGN KEY (comment_id) REFERENCES comment (id),
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS friendship (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            friend_id INTEGER NOT NULL,
            status VARCHAR(20) NOT NULL,
            created_at DATETIME NOT NULL,
            UNIQUE(user_id, friend_id),
            FOREIGN KEY (user_id) REFERENCES user (id),
            FOREIGN KEY (friend_id) REFERENCES user (id)
        )
        ''',
        '''
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
        '''
    ]

    # Execute all table creation statements
    created_tables = []
    for table_sql in tables_to_create:
        try:
            cursor.execute(table_sql)
            table_name = table_sql.split()[5]  # Extract table name from CREATE statement
            created_tables.append(table_name)
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    # Commit and close
    conn.commit()
    conn.close()

    print("Database initialization completed!")
    print(f"Created tables: {', '.join(created_tables)}")
    return True

if __name__ == "__main__":
    initialize_database()