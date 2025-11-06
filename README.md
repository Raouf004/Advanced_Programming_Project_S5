# Social Media Backend API

A complete RESTful API for a social media platform built with FastAPI, SQLAlchemy, and JWT authentication.

## Features

- 🔐 User authentication (register, login with JWT)
- 👤 User profiles (view, update)
- 📝 Posts (create, read, update, delete)
- ❤️ Like/unlike posts
- 💬 Comments on posts
- 👥 Follow/unfollow users
- 📰 Personalized feed

## Tech Stack

- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Database (easily switchable to PostgreSQL/MySQL)
- **JWT** - Secure authentication
- **Pydantic** - Data validation
- **Bcrypt** - Password hashing

## Installation

1. Clone the repository
```bash
git clone 
cd social-media-backend
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```bash
# Copy .env file and update with your settings
cp .env.example .env
```

5. Run the application
```bash
python run.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure