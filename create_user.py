from app import create_app, db, bcrypt
from app.models import User

app = create_app()

with app.app_context():
    # Create a test user
    user = User(
        username='test',
        email='test@example.com',
        first_name='Test',
        last_name='User',
        location='Test City'
    )
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    print("User created successfully!")