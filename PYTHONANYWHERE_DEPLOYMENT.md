# PythonAnywhere Deployment Guide

This guide will help you deploy your Flask application to PythonAnywhere.

## Prerequisites
1. A PythonAnywhere account (free available at pythonanywhere.com)

## Steps to Deploy

### 1. Sign Up for PythonAnywhere
1. Go to https://www.pythonanywhere.com/
2. Click "Pricing" 
3. Select "Beginner" (free plan)
4. Sign up with your email or GitHub

### 2. Get Your Code on PythonAnywhere
1. After logging in, click "Consoles" tab
2. Click "Bash" to start a new console
3. Run these commands:
   ```bash
   git clone https://github.com/mavemake/WebTest.git
   cd WebTest
   ```

### 3. Set Up Virtual Environment
1. In the same console, run:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### 4. Create Web App
1. Click "Web" tab at the top
2. Click "Add a new web app"
3. Click "Next"
4. Choose "Manual configuration" 
5. Select Python 3.12
6. Click "Next"

### 5. Configure Virtual Environment
1. In the "Virtualenv" section, enter: `venv`
2. Press Enter (it will auto-complete to the full path)

### 6. Configure WSGI File
1. Click the link next to "WSGI configuration file"
2. Delete everything in the file
3. Replace with the contents of `pythonanywhere_wsgi.py` from your repository
4. Remember to replace "yourusername" with your actual PythonAnywhere username

### 7. Add Environment Variables
1. Scroll down to "Environment variables"
2. Add:
   - Key: `SECRET_KEY`, Value: (generate a random string)
   - Key: `FLASK_ENV`, Value: `production`

### 8. Reload and Test
1. Click the green "Reload" button at the top
2. Click the link to your site (yourusername.pythonanywhere.com)

## Troubleshooting Tips

If you encounter issues:
1. Check that the paths in the WSGI file are correct
2. Ensure all dependencies are installed in the virtual environment
3. Verify environment variables are set correctly
4. Check the error logs in the PythonAnywhere dashboard