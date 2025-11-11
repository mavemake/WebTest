# Deployment Guide

This guide will help you deploy the Single Mothers Connect application to Render.

## Prerequisites

1. A GitHub account
2. A Render account (free available at render.com)

## Steps to Deploy

### 1. Prepare Your Repository

1. Create a new repository on GitHub
2. Push your code to the repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin main
   ```

### 2. Create a Render Account

1. Go to https://render.com and sign up for a free account
2. Connect your GitHub account to Render

### 3. Deploy to Render

1. Click "New+" and select "Web Service"
2. Connect to your GitHub repository
3. Configure the following settings:
   - Name: single-mothers-connect (or any name you prefer)
   - Region: Choose the region closest to your users
   - Branch: main
   - Root Directory: Leave empty
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn run:app`

### 4. Configure Environment Variables

In the "Advanced" section, add the following environment variables:

- SECRET_KEY: Generate a strong secret key
- FLASK_ENV: production

### 5. Deploy

Click "Create Web Service" and wait for the deployment to complete.

## Database Considerations

For production, consider using PostgreSQL instead of SQLite:

1. Add a PostgreSQL database in Render
2. Update the DATABASE_URL environment variable to point to your PostgreSQL database
3. Update your requirements.txt to include psycopg2-binary:
   ```
   psycopg2-binary==2.9.7
   ```

## Custom Domain (Optional)

1. In your Render dashboard, go to your web service
2. Click on "Settings"
3. Scroll down to "Custom Domains"
4. Follow the instructions to add your custom domain

## Monitoring and Logs

Render provides built-in logging and monitoring:

1. Go to your web service dashboard
2. Click on "Logs" to view real-time logs
3. Set up alerts if needed

## Scaling

Render automatically scales your application based on traffic. For more control:

1. Go to your web service dashboard
2. Click on "Settings"
3. Adjust the instance count and type as needed

## Troubleshooting

If you encounter issues:

1. Check the logs in the Render dashboard
2. Ensure all environment variables are set correctly
3. Verify your requirements.txt includes all necessary dependencies
4. Make sure your Procfile is correctly formatted
