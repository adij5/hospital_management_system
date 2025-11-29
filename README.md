# hospital_management_system
Hospital Management System built with Flask and PostgreSQL.
Includes: patient CRUD, appointment scheduling, simple staff login, and database initialization.

## Features
- Flask backend with SQLAlchemy (PostgreSQL)
- Models: User (staff), Patient, Appointment
- Simple HTML templates (Jinja2)
- Init script to create database tables and seed sample data
- Configurable via `DATABASE_URL` environment variable
- Ready for GitHub — copy files and push

## Requirements
- Python 3.8+
- PostgreSQL server
- Create a database (example): `createdb hms_db`

Install dependencies:

```bash
pip install -r requirements.txt
```

Set environment variables:

```bash
export DATABASE_URL='postgresql://postgres:password@localhost:5432/hms_db'
export FLASK_APP=app.py
export FLASK_ENV=development
export SECRET_KEY='a-strong-secret-key'
```

Initialize the database and seed sample data:

```bash
python init_db.py
```

Run the app:

```bash
flask run
# or
python app.py
```

## Files
- `app.py` — Flask application with routes
- `models.py` — SQLAlchemy models
- `config.py` — configuration helper
- `init_db.py` — creates tables and seeds sample data
- `templates/` — Jinja2 HTML templates
- `static/` — CSS
- `requirements.txt`, `.gitignore`, `LICENSE`

## Notes
- For production use, run behind a WSGI server (gunicorn) and secure secrets.
- The app expects a running PostgreSQL instance reachable by `DATABASE_URL`.
