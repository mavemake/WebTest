from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from app import db, bcrypt
from .friendship import Friendship

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    profile_image = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(60), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100))
    bio = db.Column(db.Text)
    children_count = db.Column(db.Integer, default=0)
    partners_count = db.Column(db.Integer, default=0)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy=True, cascade='all, delete-orphan')
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', back_populates='sender', lazy=True)
    received_messages = db.relationship('Message', foreign_keys='Message.recipient_id', back_populates='recipient', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.first_name} {self.last_name}')"
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def get_friendship_with(self, other_user):
        """Get the friendship status between this user and another user"""
        # Check if other_user is anonymous
        if not hasattr(other_user, 'id'):
            return None
            
        if self.id == other_user.id:
            return None
            
        friendship = Friendship.query.filter(
            db.or_(
                db.and_(Friendship.user_id == self.id, Friendship.friend_id == other_user.id),
                db.and_(Friendship.user_id == other_user.id, Friendship.friend_id == self.id)
            )
        ).first()
        
        return friendship

    def is_friends_with(self, other_user):
        """Check if this user is friends with another user"""
        friendship = self.get_friendship_with(other_user)
        return friendship and friendship.status == 'accepted'
