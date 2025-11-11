# Single Mothers Connect - Flask Application

A social networking platform for single mothers, built with Flask.

## Features

- User registration and authentication
- Profile management
- Posting and commenting
- Like functionality
- Private messaging
- Notifications
- Search functionality

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up the database:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```
5. Run the application:
   ```
   python run.py
   ```

## Database Initialization

If you encounter database errors or missing tables, you can initialize the database with all required tables using:

```
python init_database.py
```

This script will create all missing tables while preserving existing data.

## Deployment

This application is ready for deployment to platforms like Render, Heroku, or similar services.

Key deployment files:

- `Procfile`: Contains the command to run the application with Gunicorn
- `requirements.txt`: Updated with gunicorn for production deployment
- `runtime.txt`: Specifies Python version (3.12)

Deployment steps:

1. Push your code to a GitHub repository
2. Connect your repository to your preferred deployment platform
3. Set environment variables (SECRET_KEY, DATABASE_URL)
4. Deploy the application

For production, consider using PostgreSQL instead of SQLite for better performance and reliability.

## Usage

Visit `http://localhost:5000` in your browser to access the application.

## API Endpoints

- `/api/posts` - Get all posts
- `/api/posts/<int:post_id>` - Get a specific post
- `/api/users/<int:user_id>` - Get user information
- `/api/users/<int:user_id>/posts` - Get posts by a specific user
- `/api/notifications` - Get notifications for the current user
- `/api/messages/<int:user_id>` - Get messages between current user and another user

## Technologies Used

- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- Bootstrap 5
- SQLite
