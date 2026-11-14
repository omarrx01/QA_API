# QA API

A RESTful Question & Answer API built with FastAPI, PostgreSQL, Redis, Docker, and Alembic.

## Features

- Create and retrieve questions and answers
- PostgreSQL database with UUID primary keys
- Redis caching with a 1-hour TTL
- Automatic fallback to PostgreSQL when Redis is unavailable
- Database migrations using Alembic
- Docker Compose with PostgreSQL, Redis, and FastAPI
- Container health checks
- Persistent PostgreSQL storage
- Multi-stage Docker build
- Non-root Docker user
- GitHub Actions CI/CD publishing to Docker Hub

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL 16
- Redis 7
- Alembic
- Docker and Docker Compose
- GitHub Actions
- uv

## Project Structure

    QA_API/
    ├── api/
    │   ├── main.py
    │   ├── models.py
    │   ├── schemas.py
    │   ├── database.py
    │   └── cache.py
    ├── migrations/
    │   └── versions/
    ├── .github/
    │   └── workflows/
    │       └── docker-publish.yml
    ├── Dockerfile
    ├── docker-compose.yml
    ├── alembic.ini
    ├── .env.example
    ├── pyproject.toml
    └── README.md

## Getting Started

### 1. Clone the repository

    git clone https://github.com/omarrx01/QA_API.git
    cd QA_API

### 2. Configure environment variables

Copy `.env.example` to `.env` and configure the PostgreSQL credentials.

### 3. Start the application

    docker compose up -d --build

Docker Compose starts PostgreSQL, Redis, and FastAPI.

Alembic applies pending migrations before FastAPI starts.

### 4. Access the API

Swagger UI:

http://localhost:8000/docs

Health endpoint:

http://localhost:8000/health

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | API welcome message |
| POST | /questions | Create a question and answer |
| GET | /questions/{question_id} | Retrieve a record by UUID |
| GET | /answers?question=... | Retrieve an answer using Redis or PostgreSQL |
| GET | /health | Check API health |

## Example Request

POST /questions

    {
      "question": "What is Redis?",
      "answer": "Redis is an in-memory data store."
    }

## Redis Caching

The API checks Redis before querying PostgreSQL.

- Cache hit: Return the cached answer.
- Cache miss: Query PostgreSQL and cache the result.
- Redis unavailable: Continue using PostgreSQL.
- Cache expiration: 3600 seconds (1 hour).

## Database Migrations

Check the current migration:

    docker compose exec backend alembic current

Apply pending migrations:

    docker compose exec backend alembic upgrade head

## Docker Hub

Published Docker image:

https://hub.docker.com/r/omarrx04/qa-api

Pull the image:

    docker pull omarrx04/qa-api:latest

## CI/CD

GitHub Actions automatically builds and pushes the Docker image to Docker Hub when changes are pushed to the main branch.

## Author

Omar Haitham

GitHub: https://github.com/omarrx01
