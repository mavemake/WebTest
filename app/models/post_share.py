from datetime import datetime
from app import db

class PostShare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shared_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    share_content = db.Column(db.Text)  # Optional content when sharing
    
    # Relationships
    post = db.relationship('Post', backref=db.backref('shares', lazy=True))
    user = db.relationship('User', backref=db.backref('shared_posts', lazy=True))
    
    def __repr__(self):
        return f"PostShare('{self.user.username}', '{self.post.id}', '{self.shared_at}')"