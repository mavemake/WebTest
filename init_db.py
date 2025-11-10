from app import create_app, db
from app.models import User, Post, Comment, Message, Notification, PostLike

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    print("Database tables created successfully!")