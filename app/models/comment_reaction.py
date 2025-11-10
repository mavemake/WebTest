from datetime import datetime
from app import db

class CommentReaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reaction_type = db.Column(db.String(20), nullable=False)  # heart, wow, angry, hahaha
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    comment = db.relationship('Comment', backref=db.backref('reactions', lazy=True))
    user = db.relationship('User', backref=db.backref('comment_reactions', lazy=True))
    
    def __repr__(self):
        return f"CommentReaction('{self.reaction_type}', '{self.comment.id}', '{self.user.username}')"