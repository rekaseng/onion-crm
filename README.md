
#  Onion CRM Backend  
A backend built using **FastAPI**, **Poetry**, **Alembic**, and **PostgreSQL**, following a clean `/src` architecture.

This guide provides everything you need to install, run, and maintain the backend.

---

## 📦 1. Installation

### Install Poetry (if not already installed)

```bash
pip install poetry
```

### Install project dependencies
Inside the project folder:

```bash
poetry install
```
This will install everything required from pyproject.toml.

### Enter the Poetry virtual environment

```bash
poetry shell
```

## 🐍 2. Set PYTHONPATH

The project uses a clean /src folder structure.
Set the environment variable before running the app or Alembic migrations.

## 🗄️ 3. Database Migration (Alembic)
### Step 1 — Create your model
Create your new model inside:
```bash
src/models/<model_name>.py
```

### Step 2 — Import model into Alembic environment
Edit:
```bash
alembic/env.py
```
Add your new model import so Alembic can detect schema changes.

## Generate a migration file

### Windows (PowerShell)
```bash
$env:PYTHONPATH="src"
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
alembic revision --autogenerate --rev-id=$timestamp -m "add_model"
```
### Linux / macOS
```bash
export PYTHONPATH=src
alembic revision --autogenerate --rev-id=$(date +%Y%m%d%H%M%S) -m "add_model"
```
NOTE: Your Alembic connection string should NOT contain asyncpg.
Only the running FastAPI app should use asyncpg, not Alembic.
### Apply migration to database
```bash
alembic upgrade head
```
### Revert last migration
```bash
alembic downgrade -1
```
## ▶️ 4. Running the Application
### Step 1 — Create .env
Copy:
```bash
.env.sample → .env
```
Fill in your database credentials and application settings.

### Step 2 — Start the FastAPI server (with auto reload)
### Windows (PowerShell)
```bash
$env:PYTHONPATH="src"
poetry shell
uvicorn main:app --reload
```
### Linux / macOS
```bash
export PYTHONPATH=src
poetry shell
uvicorn main:app --reload
```
FastAPI will now serve at:
➡️ http://127.0.0.1:8000

➡️ Swagger docs: http://127.0.0.1:8000/docs

## 🧪 5. Running Tests
Set PYTHONPATH first (same instructions above), then:
```bash
pytest
```