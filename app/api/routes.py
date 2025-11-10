from flask import jsonify, request
from flask_login import login_required, current_user
from app import db
from app.api import api
from app.models import User, Post, Comment, Message, Notification, PostLike

@api.route('/posts')
def get_posts():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return jsonify([{
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'date_posted': post.date_posted.isoformat(),
        'author': {
            'id': post.author.id,
            'username': post.author.username,
            'first_name': post.author.first_name,
            'last_name': post.author.last_name,
            'location': post.author.location
        },
        'like_count': post.like_count(),
        'comment_count': len(post.comments)
    } for post in posts])

@api.route('/posts/<int:post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'date_posted': post.date_posted.isoformat(),
        'author': {
            'id': post.author.id,
            'username': post.author.username,
            'first_name': post.author.first_name,
            'last_name': post.author.last_name,
            'location': post.author.location
        },
        'like_count': post.like_count(),
        'comments': [{
            'id': comment.id,
            'content': comment.content,
            'date_posted': comment.date_posted.isoformat(),
            'author': {
                'id': comment.author.id,
                'username': comment.author.username,
                'first_name': comment.author.first_name,
                'last_name': comment.author.last_name
            }
        } for comment in post.comments]
    })

@api.route('/users/<int:user_id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'location': user.location,
        'bio': user.bio,
        'children_count': user.children_count,
        'date_joined': user.date_joined.isoformat(),
        'post_count': len(user.posts)
    })

@api.route('/users/<int:user_id>/posts')
def get_user_posts(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).all()
    return jsonify([{
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'date_posted': post.date_posted.isoformat(),
        'like_count': post.like_count(),
        'comment_count': len(post.comments)
    } for post in posts])

@api.route('/notifications')
@login_required
def get_notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.timestamp.desc()).all()
    return jsonify([{
        'id': notification.id,
        'content': notification.content,
        'timestamp': notification.timestamp.isoformat(),
        'is_read': notification.is_read,
        'notification_type': notification.notification_type
    } for notification in notifications])

@api.route('/messages/<int:user_id>')
@login_required
def get_messages(user_id):
    messages = Message.query.filter(
        db.or_(
            db.and_(Message.sender_id == current_user.id, Message.recipient_id == user_id),
            db.and_(Message.sender_id == user_id, Message.recipient_id == current_user.id)
        )
    ).order_by(Message.timestamp.asc()).all()
    
    return jsonify([{
        'id': message.id,
        'content': message.content,
        'timestamp': message.timestamp.isoformat(),
        'sender_id': message.sender_id,
        'recipient_id': message.recipient_id,
        'is_read': message.is_read
    } for message in messages])