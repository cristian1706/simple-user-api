# SimpleUser Management API

A FastAPI-based REST API for user management with JWT authentication, SQLite database, and Docker support.

## Features

- User registration and login with JWT authentication
- Simple frontend for registration using Jinja2 templates
- CRUD operations for user profiles
- Dockerized setup (development and production environments)
- Clean, modular project structure
- Auto-generated API documentation
- Well-documented code
- SQLite database
- Alembic migrations

## Requirements

- Python 3.10+
- Docker and Docker Compose (optional)

## Project Structure

```
simple_user_api/
├── alembic/                  # Migration scripts
├── app/
│   ├── api/                  # API routes
│   ├── core/                 # Core modules
│   ├── db/                   # Database setup
│   ├── models/               # SQLAlchemy models
│   ├── schemas/              # Pydantic schemas
│   ├── static/               # Static files
│   ├── templates/            # Jinja2 templates
│   └── main.py               # FastAPI application
├── tests/                    # Pytest tests
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose configuration
├── alembic.ini               # Alembic configuration
└── requirements.txt          # Project dependencies
```

## Setup Instructions

### Local Development

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd simple-user-api
   ```

2. Create and activate a virtual environment (pyenv is recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python run.py
   ```

5. Access the application:
   - API: http://localhost:8000/api/v1
   - Documentation: http://localhost:8000/api/v1/docs
   - Registration page: http://localhost:8000/

### Using Docker

1. Build and run the development environment:
   ```bash
   docker-compose up --build app-dev
   ```

2. Or build and run the production environment:
   ```bash
   docker-compose up --build app-prod
   ```

3. Access the application:
   - Development: http://localhost:8000
   - Production: http://localhost:8001

## API Endpoints

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/users/me` - Get current user info (requires JWT)
- `PUT /api/v1/users/me` - Update user profile (requires JWT)
- `DELETE /api/v1/users/me` - Delete user account (requires JWT)

## Database Migrations

Initialize the database:
```bash
alembic upgrade head
```

Create a new migration after model changes:
```bash
alembic revision --autogenerate -m "Description of changes"
```

## Running Tests

```bash
pytest -v tests/test_auth.py
pytest -v tests/test_users.py
```

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- Rate limiting on registration endpoint (3 requests/minute)


## TODO
- add more tests
- add pre-commit (flake8, black formatter, isort, etc)
- add github actions and testing pipeline
- add coverage
- replace pip for poetry or uv
