from datetime import datetime
from app import db

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)  # Reference to the post that triggered the notification
    is_read = db.Column(db.Boolean, default=False)
    notification_type = db.Column(db.String(50), nullable=False)  # like, comment, follow, etc.
    
    # Relationship
    post = db.relationship('Post', backref=db.backref('notifications', lazy=True))
    
    def __repr__(self):
        return f"Notification('{self.content[:20]}...', '{self.timestamp}')"