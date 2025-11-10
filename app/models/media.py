from datetime import datetime
from app import db

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    media_type = db.Column(db.String(10), nullable=False)  # 'image' or 'video'
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    post = db.relationship('Post', back_populates='media_files')
    comment = db.relationship('Comment', back_populates='media_files')
    
    def __repr__(self):
        return f"Media('{self.filename}', '{self.media_type}')"