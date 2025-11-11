"""
WSGI configuration file for PythonAnywhere deployment
This file should be used when deploying to PythonAnywhere
"""
import sys
import os

# Add your project directory to the sys.path
path = '/home/yourusername/WebTest'
if path not in sys.path:
    sys.path.insert(0, path)

# Change to your project directory
os.chdir(path)

# Import your Flask application
from run import application

# For debugging purposes only - remove in production
# print("Python path:", sys.path)
# print("Current working directory:", os.getcwd())