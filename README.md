<div id="top"></div>

# Ekimo Assignment – FastAPI

## About The Project

This is a FastAPI application that lets users upload product data using CSV or Excel files. It stores the data in a PostgreSQL database and automatically syncs any changes to an external API every 10 minutes. The app includes user registration and login, background job scheduling, and a clean project structure with support for testing, code formatting, and database migrations. Swagger documentation is available at /docs for easy testing and development.

## Built With

* [FastAPI](https://fastapi.tiangolo.com/) – Web framework for building APIs
* [uv](https://github.com/astral-sh/uv) – Ultra-fast Python package manager
* [PostgreSQL](https://www.postgresql.org/) – Open-source relational database
* [SQLAlchemy](https://www.sqlalchemy.org/) – ORM for database models and queries
* [Alembic](https://alembic.sqlalchemy.org/) – Database migrations tool
* [Docker](https://www.docker.com/) – Containerization platform
* [APScheduler](https://apscheduler.readthedocs.io/en/stable/) – Job scheduling for background tasks
* [pytest](https://docs.pytest.org/) – Testing framework
* [Ruff](https://docs.astral.sh/ruff/) – Fast Python linter and formatter
* [Mypy](https://mypy-lang.org/) – Static type checker
* [GitHub Actions](https://github.com/features/actions) – CI/CD automation

---

## Getting Started

### Prerequisites

You must have Python 3.11+ and [uv](https://github.com/astral-sh/uv) installed:

```bash
pip install uv
```

### Installation

Clone the repository:

```bash
git clone https://github.com/AiKay96/ekimo-assignment.git
cd ekimo-assignment
```

Install dependencies:

```bash
make install
```

---

## Usage

### Local Execution

To start the application with background sync enabled:

```bash
make run
```

You can also manually trigger the synchronization job:

```bash
make sync
```

### Docker

To build and run using Docker:

```bash
make build
make up
```

---

## Development Commands

### Formatting and Linting

```bash
make format         # Format using Ruff
make lint           # Run format check, linter, and type checker
```

### Testing

```bash
make test           # Unit & integration tests
make test-e2e       # End-to-end tests
```

---

## Database Migrations

To apply migrations:

```bash
alembic upgrade head
```

---
## Environment Variables

This project uses a `.env` file for configuration. Before running the app, create the file.

### Description

| Variable                  | Description                                    |
|---------------------------|------------------------------------------------|
| `DATABASE_URL`            | PostgreSQL connection string                   |
| `TEST_DATABASE_URL`       | Connection string for test database            |
| `SECRET_KEY`              | Secret key used to sign JWT tokens             |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT access token expiration in minutes     |
| `SYNC_INTERVAL_MINUTES`   | Background sync interval in minutes            |
| `USERNAME`, `PASSWORD`    | Credentials for auth while sync.          |
| `BASE_URL`                | Base API URL (used by the sync job)            |

> These variables are automatically loaded when using Docker.

---

## Docker Image (Prebuilt)

A prebuilt Docker image is available: [package](https://github.com/AiKay96/ekimo-assignment/pkgs/container/ekimo)

You can run it directly or use it as a base image for deployment.

## API Overview

### Users

| Method | Endpoint | Description     |
|--------|----------|-----------------|
| POST   | /users   | Register a user |

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | /auth    | Login       |

### Products

| Method | Endpoint   | Description                  |
|--------|------------|------------------------------|
| PUT    | /products  | Upload product data          |
| POST   | /products  | Sync flagged product records |

---

## Detailed Description

- **User Management**: Anyone can register a user using the `/users` endpoint. Authentication is done via `/auth` using secure ciphered tokens (JWT).

- **Product Upload**: Authenticated users can upload product data via CSV or XLSX files to the `/products` endpoint (PUT). The server parses and creates/updates entries in the database.

- **Synchronization**: A background job runs every 10 minutes (by default) and filters newly updated/created products. These are sent to `/products` (POST) for "external" API sync.

- **Testing**: The project includes high-quality unit, integration, and end-to-end tests. Coverage is high.

---

## GitHub Actions CI

The project uses GitHub Actions to run a full CI suite on every push:

- ✅ Linting
- ✅ E2E Tests
- ✅ Core (Unit / Integration) Tests
- ✅ Docker Build

---
