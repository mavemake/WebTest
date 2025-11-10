from app import create_app
from config import Config

# Automatically initialize database if needed
try:
    from auto_init_db import init_db_if_needed
    init_db_if_needed()
except Exception as e:
    print(f"Warning: Could not initialize database automatically: {e}")

application = create_app()

if __name__ == '__main__':
    application.run(debug=False)