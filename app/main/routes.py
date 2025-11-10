from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.main import main
from app.models import User, Post, Comment, Message, Notification, PostLike, PostShare, CommentReaction, Friendship, Media
from app.forms import RegistrationForm, LoginForm, PostForm, CommentForm, MessageForm, EditProfileForm
from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename

def get_all_posts_ordered():
    """Get all posts (original and shared) ordered by date"""
    if not current_user.is_authenticated:
        # For non-authenticated users, show only original posts
        original_posts = Post.query.all()
        return sorted(original_posts, key=lambda x: x.date_posted, reverse=True)
    
    # Get original posts from friends and self
    # First get all friends (both directions)
    friendships = Friendship.query.filter(
        db.or_(
            Friendship.user_id == current_user.id,
            Friendship.friend_id == current_user.id
        )
    ).filter(Friendship.status == 'accepted').all()
    
    # Get friend user IDs
    friend_ids = []
    for friendship in friendships:
        if friendship.user_id == current_user.id:
            friend_ids.append(friendship.friend_id)
        else:
            friend_ids.append(friendship.user_id)
    
    # Always include self
    friend_ids.append(current_user.id)
    
    # Get original posts from friends and self
    original_posts = Post.query.filter(Post.user_id.in_(friend_ids)).all()
    
    # Get shared posts from friends and self
    shared_posts = []
    post_shares = PostShare.query.filter(PostShare.user_id.in_(friend_ids)).all()
    
    for share in post_shares:
        # Create a pseudo post object for the shared post
        shared_post = type('Post', (object,), {
            'id': share.post.id,
            'title': share.post.title,
            'content': share.share_content if share.share_content else share.post.content,
            'date_posted': share.shared_at,
            'author': share.user,  # The user who shared it
            'original_author': share.post.author,  # The original author
            'media_files': share.post.media_files,
            'comments': share.post.comments,
            'likes': share.post.likes,
            'like_count': share.post.like_count,
            'share_count': share.post.share_count,
            'is_shared': True,
            'original_post': share.post
        })
        shared_posts.append(shared_post)
    
    # Combine and sort all posts by date
    all_posts = original_posts + shared_posts
    all_posts.sort(key=lambda x: x.date_posted, reverse=True)
    
    return all_posts

@main.route("/")
@main.route("/home")
def home():
    # Get all posts ordered by date
    page = request.args.get('page', 1, type=int)
    all_posts = get_all_posts_ordered()
    
    # Manual pagination
    per_page = 5
    total = len(all_posts)
    pages = (total + per_page - 1) // per_page
    has_prev = page > 1
    has_next = page < pages
    prev_num = page - 1 if has_prev else None
    next_num = page + 1 if has_next else None
    
    # Get posts for current page
    start = (page - 1) * per_page
    end = start + per_page
    posts_for_page = all_posts[start:end]
    
    # Create a pagination-like object
    from collections import namedtuple
    Pagination = namedtuple('Pagination', ['items', 'page', 'pages', 'has_prev', 'has_next', 'prev_num', 'next_num'])
    posts = Pagination(posts_for_page, page, pages, has_prev, has_next, prev_num, next_num)
    
    # Check if request is AJAX for infinite scroll
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return only the posts for AJAX requests
        return render_template('home_posts.html', posts=posts)
    
    return render_template('home.html', posts=posts)

@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user already exists
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email already registered. Please login.', 'danger')
            return redirect(url_for('main.login'))
        
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            location=form.location.data,
            children_count=form.children_count.data,
            partners_count=form.partners_count.data,
            bio=form.bio.data
        )
        user.set_password(form.password.data)
        
        # Handle profile image upload
        if form.profile_image.data:
            profile_image = form.profile_image.data
            if profile_image.filename:
                # Generate unique filename
                filename = secure_filename(profile_image.filename)
                unique_filename = str(uuid.uuid4()) + '_' + filename
                # Create user-specific folder
                user_folder = os.path.join(current_app.root_path, 'static', 'uploads', str(user.id))
                upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', str(user.id))
                
                # Ensure user-specific upload directory exists
                os.makedirs(upload_folder, exist_ok=True)
                
                # Save file
                image_path = os.path.join(upload_folder, unique_filename)
                profile_image.save(image_path)
                
                # Store relative path in database
                user.profile_image = f'uploads/{user.id}/{unique_filename}'
        
        db.session.add(user)
        db.session.commit()
        
        flash('Your account has been created! You can now login.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html', title='Register', form=form)

@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('login.html', title='Login', form=form)

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route("/profile/<username>")
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    
    # Get original posts by this user
    original_posts = Post.query.filter(Post.user_id == user.id).order_by(Post.date_posted.desc())
    
    # Get posts shared by this user
    shared_posts_query = db.session.query(Post).join(PostShare).filter(PostShare.user_id == user.id)
    
    # Combine original and shared posts
    # Note: We need to execute the queries to combine them properly
    all_original_posts = original_posts.all()
    
    # For shared posts, we need to create pseudo post objects
    shared_posts = []
    post_shares = PostShare.query.filter(PostShare.user_id == user.id).all()
    
    for share in post_shares:
        # Create a pseudo post object for the shared post
        shared_post = type('Post', (object,), {
            'id': share.post.id,
            'title': share.post.title,
            'content': share.share_content if share.share_content else share.post.content,
            'date_posted': share.shared_at,
            'author': share.user,  # The user who shared it
            'original_author': share.post.author,  # The original author
            'media_files': share.post.media_files,
            'comments': share.post.comments,
            'likes': share.post.likes,
            'like_count': share.post.like_count,
            'share_count': share.post.share_count,
            'is_shared': True,
            'original_post': share.post
        })
        shared_posts.append(shared_post)
    
    # Combine and sort all posts by date
    all_posts = all_original_posts + shared_posts
    all_posts.sort(key=lambda x: x.date_posted, reverse=True)
    
    # Manual pagination for combined posts
    per_page = 5
    total = len(all_posts)
    pages = (total + per_page - 1) // per_page
    has_prev = page > 1
    has_next = page < pages
    prev_num = page - 1 if has_prev else None
    next_num = page + 1 if has_next else None
    
    # Get posts for current page
    start = (page - 1) * per_page
    end = start + per_page
    posts_for_page = all_posts[start:end]
    
    # Create a pagination-like object
    from collections import namedtuple
    Pagination = namedtuple('Pagination', ['items', 'page', 'pages', 'has_prev', 'has_next', 'prev_num', 'next_num'])
    posts = Pagination(posts_for_page, page, pages, has_prev, has_next, prev_num, next_num)
    
    return render_template('profile.html', user=user, posts=posts)

@main.route("/profile/edit", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.location = form.location.data
        current_user.children_count = form.children_count.data
        current_user.partners_count = form.partners_count.data
        current_user.bio = form.bio.data
        
        # Handle profile image upload
        if form.profile_image.data:
            profile_image = form.profile_image.data
            if profile_image.filename:
                # Generate unique filename
                filename = secure_filename(profile_image.filename)
                unique_filename = str(uuid.uuid4()) + '_' + filename
                # Create user-specific folder
                user_folder = os.path.join(current_app.root_path, 'static', 'uploads', str(current_user.id))
                upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', str(current_user.id))
                
                # Ensure user-specific upload directory exists
                os.makedirs(upload_folder, exist_ok=True)
                
                # Save file
                image_path = os.path.join(upload_folder, unique_filename)
                profile_image.save(image_path)
                
                # Store relative path in database
                current_user.profile_image = f'uploads/{current_user.id}/{unique_filename}'
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.profile', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.location.data = current_user.location
        form.children_count.data = current_user.children_count
        form.partners_count.data = current_user.partners_count
        form.bio.data = current_user.bio
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@main.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        content = request.form.get('content')
        media_files = request.files.getlist('media')
        
        if not content:
            flash('Post content is required!', 'danger')
            return redirect(url_for('main.new_post'))
        
        # Create post
        post = Post(
            content=content,
            author=current_user
        )
        db.session.add(post)
        db.session.flush()  # Get post ID for media files
        
        # Handle multiple media uploads
        for media in media_files:
            if media and media.filename:
                # Generate unique filename
                filename = secure_filename(media.filename)
                unique_filename = str(uuid.uuid4()) + '_' + filename
                # Create user-specific folder
                upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', str(current_user.id))
                
                # Ensure user-specific upload directory exists
                os.makedirs(upload_folder, exist_ok=True)
                
                # Save file
                media_path = os.path.join(upload_folder, unique_filename)
                media.save(media_path)
                
                # Determine media type
                if media.content_type.startswith('image/'):
                    media_type = 'image'
                elif media.content_type.startswith('video/'):
                    media_type = 'video'
                else:
                    media_type = 'other'
                
                # Create media record
                media_record = Media(
                    filename=f'/static/uploads/{current_user.id}/{unique_filename}',
                    media_type=media_type,
                    post_id=post.id
                )
                db.session.add(media_record)
        
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    
    return render_template('create_post.html', title='New Post', legend='New Post')

@main.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    comments = Comment.query.filter_by(post_id=post.id, parent_id=None).order_by(Comment.date_posted.desc()).all()
    return render_template('post.html', title=post.title, post=post, form=form, comments=comments)

@main.route("/post/<int:post_id>/comment", methods=['POST'])
@login_required
def comment_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            author=current_user,
            post=post
        )
        
        # Handle multiple media uploads
        media_files = request.files.getlist('media')
        for media in media_files:
            if media and media.filename:
                # Generate unique filename
                filename = secure_filename(media.filename)
                unique_filename = str(uuid.uuid4()) + '_' + filename
                # Create user-specific folder
                upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', str(current_user.id))
                
                # Ensure user-specific upload directory exists
                os.makedirs(upload_folder, exist_ok=True)
                
                # Save file
                media_path = os.path.join(upload_folder, unique_filename)
                media.save(media_path)
                
                # Determine media type
                if media.content_type.startswith('image/'):
                    media_type = 'image'
                elif media.content_type.startswith('video/'):
                    media_type = 'video'
                else:
                    media_type = 'other'
                
                # Create media record
                media_record = Media(
                    filename=f'/static/uploads/{current_user.id}/{unique_filename}',
                    media_type=media_type,
                    comment_id=comment.id
                )
                db.session.add(media_record)
        
        db.session.add(comment)
        db.session.commit()
        
        # Create notification for post author (if not the commenter)
        if post.author.id != current_user.id:
            notification = Notification(
                content=f"{current_user.first_name} {current_user.last_name} commented on your post",
                user=post.author,
                post_id=post.id,
                notification_type='comment'
            )
            db.session.add(notification)
            db.session.commit()
        
        flash('Your comment has been added!', 'success')
    return redirect(url_for('main.post', post_id=post.id))

@main.route("/post/<int:post_id>/like", methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Check if user already liked the post
    like = PostLike.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    
    if like:
        # Unlike the post
        db.session.delete(like)
        db.session.commit()
        # Remove notification if it exists
        notification = Notification.query.filter_by(
            user_id=post.author.id,
            content=f"{current_user.first_name} {current_user.last_name} liked your post"
        ).first()
        if notification:
            db.session.delete(notification)
            db.session.commit()
    else:
        # Like the post
        like = PostLike(user_id=current_user.id, post_id=post.id)
        db.session.add(like)
        db.session.commit()
        
        # Create notification for post author (if not the liker)
        if post.author.id != current_user.id:
            notification = Notification(
                content=f"{current_user.first_name} {current_user.last_name} liked your post",
                user=post.author,
                post_id=post.id,
                notification_type='like'
            )
            db.session.add(notification)
            db.session.commit()
    
    return jsonify({'likes': post.like_count()})

@main.route("/messages")
@login_required
def messages():
    # Get conversations with other users
    sent_messages = Message.query.filter_by(sender_id=current_user.id).all()
    received_messages = Message.query.filter_by(recipient_id=current_user.id).all()
    
    # Combine and sort messages
    all_messages = sent_messages + received_messages
    all_messages.sort(key=lambda x: x.timestamp, reverse=True)
    
    # Get unique users that the current user has messaged or been messaged by
    user_ids = set()
    for message in all_messages:
        if message.sender_id != current_user.id:
            user_ids.add(message.sender_id)
        if message.recipient_id != current_user.id:
            user_ids.add(message.recipient_id)
    
    users = User.query.filter(User.id.in_(user_ids)).all()
    
    # Add unread message count for each user
    for user in users:
        user.unread_count = Message.query.filter_by(
            sender_id=user.id,
            recipient_id=current_user.id,
            is_read=False
        ).count()
    
    return render_template('messages.html', users=users)

@main.route("/messages/<int:user_id>", methods=['GET', 'POST'])
@login_required
def send_message(user_id):
    recipient = User.query.get_or_404(user_id)
    form = MessageForm()
    
    if form.validate_on_submit():
        message = Message(
            content=form.content.data,
            sender=current_user,
            recipient=recipient
        )
        db.session.add(message)
        db.session.commit()
        
        # Create notification for recipient
        notification = Notification(
            content=f"{current_user.first_name} {current_user.last_name} sent you a message",
            user=recipient,
            notification_type='message'
        )
        db.session.add(notification)
        db.session.commit()
        
        flash('Your message has been sent!', 'success')
        return redirect(url_for('main.send_message', user_id=user_id))
    
    # Get message history
    messages = Message.query.filter(
        db.or_(
            db.and_(Message.sender_id == current_user.id, Message.recipient_id == user_id),
            db.and_(Message.sender_id == user_id, Message.recipient_id == current_user.id)
        )
    ).order_by(Message.timestamp.asc()).all()
    
    # Mark received messages as read
    for message in messages:
        if message.recipient_id == current_user.id and not message.is_read:
            message.is_read = True
    db.session.commit()
    
    # Get unread count for this conversation
    unread_count = Message.query.filter_by(
        sender_id=user_id,
        recipient_id=current_user.id,
        is_read=False
    ).count()
    
    return render_template('send_message.html', title='Send Message', form=form, recipient=recipient, messages=messages, unread_count=unread_count)

@main.route("/notifications")
@login_required
def notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.timestamp.desc()).all()
    
    # Mark all as read
    for notification in notifications:
        notification.is_read = True
    db.session.commit()
    
    return render_template('notifications.html', notifications=notifications)

@main.route("/post/<int:post_id>/share", methods=['POST'])
@login_required
def share_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Check if user already shared the post
    existing_share = PostShare.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    
    if existing_share:
        # Remove share (unshare)
        db.session.delete(existing_share)
        db.session.commit()
        # Remove notification if it exists
        notification = Notification.query.filter_by(
            user_id=post.author.id,
            content=f"{current_user.first_name} {current_user.last_name} shared your post"
        ).first()
        if notification:
            db.session.delete(notification)
            db.session.commit()
    else:
        # Create new share
        share_content = request.form.get('share_content', '')
        share = PostShare(
            post_id=post.id,
            user_id=current_user.id,
            share_content=share_content
        )
        db.session.add(share)
        db.session.commit()
        
        # Create notification for post author (if not the sharer)
        if post.author.id != current_user.id:
            notification = Notification(
                content=f"{current_user.first_name} {current_user.last_name} shared your post",
                user=post.author,
                post_id=post.id,
                notification_type='share'
            )
            db.session.add(notification)
            db.session.commit()
    
    return jsonify({'shares': post.share_count()})

@main.route("/user/<int:user_id>/add_friend", methods=['POST'])
@login_required
def add_friend(user_id):
    user = User.query.get_or_404(user_id)
    
    # Check if friendship already exists
    existing_friendship = Friendship.query.filter(
        db.or_(
            db.and_(Friendship.user_id == current_user.id, Friendship.friend_id == user.id),
            db.and_(Friendship.user_id == user.id, Friendship.friend_id == current_user.id)
        )
    ).first()
    
    if existing_friendship:
        return jsonify({'message': 'Friendship request already sent or exists'}), 400
    
    # Create new friendship request
    friendship = Friendship(
        user_id=current_user.id,
        friend_id=user.id,
        status='pending'
    )
    db.session.add(friendship)
    db.session.commit()
    
    # Create notification for the user
    notification = Notification(
        content=f"{current_user.first_name} {current_user.last_name} wants to be your friend",
        user=user,
        notification_type='friend_request'
    )
    db.session.add(notification)
    db.session.commit()
    
    return jsonify({'message': 'Friend request sent successfully'})

@main.route("/user/<int:user_id>/accept_friend", methods=['POST'])
@login_required
def accept_friend(user_id):
    user = User.query.get_or_404(user_id)
    
    # Find the friendship request
    friendship = Friendship.query.filter(
        Friendship.user_id == user.id,
        Friendship.friend_id == current_user.id,
        Friendship.status == 'pending'
    ).first_or_404()
    
    # Accept the friendship
    friendship.status = 'accepted'
    db.session.commit()
    
    # Create notification for the user
    notification = Notification(
        content=f"{current_user.first_name} {current_user.last_name} accepted your friend request",
        user=user,
        notification_type='friend_accepted'
    )
    db.session.add(notification)
    db.session.commit()
    
    return jsonify({'message': 'Friend request accepted'})

@main.route("/user/<int:user_id>/reject_friend", methods=['POST'])
@login_required
def reject_friend(user_id):
    user = User.query.get_or_404(user_id)
    
    # Find the friendship request
    friendship = Friendship.query.filter(
        Friendship.user_id == user.id,
        Friendship.friend_id == current_user.id,
        Friendship.status == 'pending'
    ).first_or_404()
    
    # Delete the friendship request
    db.session.delete(friendship)
    db.session.commit()
    
    # Create notification for the user
    notification = Notification(
        content=f"{current_user.first_name} {current_user.last_name} rejected your friend request",
        user=user,
        notification_type='friend_rejected'
    )
    db.session.add(notification)
    db.session.commit()
    
    return jsonify({'message': 'Friend request rejected'})

@main.route("/comment/<int:comment_id>/reply", methods=['POST'])
@login_required
def reply_to_comment(comment_id):
    parent_comment = Comment.query.get_or_404(comment_id)
    content = request.form.get('content')
    
    if not content:
        flash('Reply content is required!', 'danger')
        return redirect(url_for('main.post', post_id=parent_comment.post_id))
    
    # Create reply comment
    reply = Comment(
        content=content,
        author=current_user,
        post=parent_comment.post,
        parent_id=parent_comment.id
    )
    db.session.add(reply)
    db.session.commit()
    
    # Create notification for parent comment author (if not the replier)
    if parent_comment.author.id != current_user.id:
        notification = Notification(
            content=f"{current_user.first_name} {current_user.last_name} replied to your comment",
            user=parent_comment.author,
            post_id=parent_comment.post_id,
            notification_type='comment_reply'
        )
        db.session.add(notification)
        db.session.commit()
    
    flash('Your reply has been added!', 'success')
    return redirect(url_for('main.post', post_id=parent_comment.post_id))

@main.route("/comment/<int:comment_id>/react", methods=['POST'])
@login_required
def react_to_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    reaction_type = request.form.get('reaction_type')
    
    # Validate reaction type
    valid_reactions = ['heart', 'wow', 'angry', 'hahaha', 'sad']
    if reaction_type not in valid_reactions:
        return jsonify({'error': 'Invalid reaction type'}), 400
    
    # Check if user already reacted to this comment with any reaction
    existing_reaction = CommentReaction.query.filter_by(
        user_id=current_user.id,
        comment_id=comment.id
    ).first()
    
    # If user already has a reaction and it's the same as the new one, remove it
    if existing_reaction and existing_reaction.reaction_type == reaction_type:
        # Remove reaction
        db.session.delete(existing_reaction)
        db.session.commit()
        action = 'removed'
    else:
        # If user has a different reaction, remove the old one first
        if existing_reaction:
            db.session.delete(existing_reaction)
        
        # Add new reaction
        reaction = CommentReaction(
            comment_id=comment.id,
            user_id=current_user.id,
            reaction_type=reaction_type
        )
        db.session.add(reaction)
        db.session.commit()
        action = 'added'
        
        # Create notification for comment author (if not the reactor)
        if comment.author.id != current_user.id:
            notification = Notification(
                content=f"{current_user.first_name} {current_user.last_name} reacted to your comment",
                user=comment.author,
                notification_type='comment_reaction'
            )
            db.session.add(notification)
            db.session.commit()
    
    # Count reactions for this comment
    reaction_counts = {}
    for reaction in valid_reactions:
        reaction_counts[reaction] = CommentReaction.query.filter_by(
            comment_id=comment.id,
            reaction_type=reaction
        ).count()
    
    return jsonify({
        'action': action,
        'reaction_counts': reaction_counts
    })

@main.route("/search")
def search():
    query = request.args.get('q')
    if query:
        users = User.query.filter(
            db.or_(
                User.username.contains(query),
                User.first_name.contains(query),
                User.last_name.contains(query)
            )
        ).all()
        posts = Post.query.filter(Post.content.contains(query)).order_by(Post.date_posted.desc()).all()
    else:
        users = []
        posts = []
    
    return render_template('search.html', users=users, posts=posts, query=query)