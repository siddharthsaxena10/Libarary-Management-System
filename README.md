# Library Management System

## Project Overview

A Library Management System backend developed using FastAPI and PostgreSQL. It manages students, administrators, books, authors, book copies, book issues, returns, and fine payments.

## Technologies Used

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Pydantic
* Swagger UI

## Features

* Student and administrator management
* Book and author management
* Book copy availability tracking
* Book issue and return management
* Fine calculation for late returns
* Fine payment record management
* Database migrations using Alembic
* API testing through Swagger UI

## Project Structure

* `app/models/` — SQLAlchemy database models
* `app/schemas/` — Pydantic request and response schemas
* `app/routes/` — API endpoints
* `app/db/` — Database connection and session setup
* `alembic/` — Database migration configuration and migration files
* `main.py` — FastAPI application entry point
* `requirements.txt` — Python dependencies

## Setup Instructions

### 1. Clone the Repository

Clone the project repository to your local machine.

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Git Bash:

```bash
source .venv/Scripts/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file and configure your PostgreSQL database connection using the environment variable expected by the application.

Do not upload database credentials or secrets to GitHub.

### 6. Apply Database Migrations

```bash
alembic upgrade head
```

### 7. Start the Application

```bash
uvicorn main:app --reload
```

### 8. Open Swagger UI

Visit:
`http://127.0.0.1:8000/docs`

## Database

PostgreSQL is used to store library records. Alembic manages database schema migrations.

## Project Status

The existing database tables and API endpoints have been created and tested locally. Further improvements and deployment can be done as needed.
