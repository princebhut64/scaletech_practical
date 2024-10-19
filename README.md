# Flask User Management API

## Introduction
This application is a Flask-based API for managing users and roles.

## Python Version
Python 3.8 and above.

## Project Structure
- `app.py`: Main application file.
- `models.py`: Database models for User and Role.
- `requirements.txt`: dependencies for the project.
- `.env`: Environment variables for secret data.
- `DATABASE_SETUP.md`: database setup file.

## Run the project locally
1. Ensure you have Python and MySQL installed.
2. **Requierments dependency**:
   ```bash
   pip install -r requirements.txt
3. **Run the project**
- `flask db init`
- `flask db migrate`
- `flask db upgrade`
- `flask run`
