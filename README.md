# Expense Tracker API

A REST API built with Flask for tracking personal expenses, with JWT authentication and Redis caching.

## Live Demo

Base URL: `https://expense-tracker-api-production-ad08.up.railway.app`

## Features

- JWT authentication with access and refresh tokens
- Role-based access control (Admin/User)
- Full CRUD on expenses
- File upload support for receipts
- Redis caching on expense retrieval for faster responses
- PostgreSQL database with SQLAlchemy ORM

## Tech Stack

- Python, Flask, Flask-RESTful
- Flask-JWT-Extended
- SQLAlchemy, PostgreSQL
- Redis
- Bcrypt, Werkzeug
- Deployed on Railway

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Create a new user |
| POST | `/login` | Get access and refresh tokens |
| POST | `/refresh` | Get a new access token |
| GET | `/expenses` | Fetch all expenses for the logged-in user |
| POST | `/expenses` | Create a new expense |
| PUT | `/expenses/<id>` | Update an expense |
| DELETE | `/expenses/<id>` | Delete an expense |

## Setup

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your `DATABASE_URL` and `REDIS_URL`
4. Run the app: `python app.py`
