# Project: Stock Trades API (Flask)

A simple REST API for managing stock trade records, built with Flask and
Flask-SQLAlchemy (SQLite backend).

## Tech Stack

- **Flask 3.1** — web framework
- **Flask-SQLAlchemy 3.1** — ORM + database integration
- **SQLite** — default database (file at `instance/db.sqlite3`, or `DATABASE_URL` env var)
- **pytest** — test framework

## Project Structure

```
app/
  __init__.py   # Application factory (create_app), db instance, init-db CLI command
  models.py     # Trade model (SQLAlchemy)
  views.py      # Route handlers for /trades endpoints (TODO)
tests/
  conftest.py   # pytest fixtures: app (in-memory SQLite), client
  helpers.py    # json_of_response helper
  test_trades.py# Tests for POST/GET /trades and /trades/<id>
requirements.txt
pytest.ini
```

## Data Model

`Trade` table (`app/models.py`):

| Column      | Type        | Notes                  |
|-------------|-------------|------------------------|
| id          | Integer PK  | autoincrement          |
| type        | String      | 'buy' or 'sell'        |
| user_id     | Integer     |                        |
| symbol      | String      | stock symbol           |
| shares      | Integer     | 10–30                  |
| price       | Integer     | price per share        |
| timestamp   | BigInteger  | epoch ms               |

## API Endpoints

| Method | Path         | Behavior                                                        |
|--------|--------------|------------------------------------------------------------------|
| POST   | /trades      | Create trade from JSON body; 201 + created object with assigned id |
| GET    | /trades      | 200 + array of all trades ordered by id ascending               |
| GET    | /trades/<id> | 200 + trade object, or 404 if not found                         |
| DELETE/PUT/PATCH | /trades/<id> | 405 (not allowed)                                   |

## Execution Flow

### Application startup

1. `flask --app app run` triggers Flask's app discovery, which calls
   `create_app()` in `app/__init__.py`.
2. `create_app()`:
   - Creates the Flask app instance.
   - Resolves the DB URI: uses `DATABASE_URL` env var if set, otherwise
     `sqlite:///instance/db.sqlite3` (creating the `instance/` dir).
   - Loads optional `app/config.py`, then calls `db.init_app(app)`.
   - Registers the `init-db` CLI command.
3. `flask --app app init-db` runs `init_db()`, which calls
   `db.drop_all()` then `db.create_all()` — this (re)creates the `trades`
   table in SQLite.
4. `flask --app app run -p 8000` starts the dev server on port 8000.

### Request flow (once implemented)

Each HTTP request is dispatched by Werkzeug's routing to the view
functions registered on the app (currently to be added in `app/views.py`):

- **POST /trades**
  1. Flask parses the JSON request body via `request.get_json()`.
  2. Build a `Trade(**payload)` model instance.
  3. `db.session.add(trade)` + `db.session.commit()`.
  4. Return the serialized trade as JSON with status 201.
- **GET /trades**
  1. Query `Trade.query.order_by(Trade.id).all()`.
  2. Serialize each model to a dict and return a JSON array with 200.
- **GET /trades/<id>**
  1. Look up `Trade.query.get_or_404(id)` (or `.get(id)` + 404 response).
  2. Return the serialized trade with 200, or 404 if missing.
- **PUT/PATCH/DELETE /trades/<id>** → automatically 405 since no routes are
  registered for those methods on the path.

### Test execution flow

1. `pytest` loads `tests/conftest.py`.
2. The `app` fixture calls `create_app()` with a `TESTING=True` config and
   `sqlite:///:memory:` URI — a fresh, isolated in-memory database per test.
3. Inside an app context, `init_db()` creates the `trades` table.
4. The `client` fixture exposes `app.test_client()`, which simulates HTTP
   requests without a running server.
5. Each test in `test_trades.py` drives the API (e.g. POST then GET) and
   asserts status codes and JSON bodies, including id ordering, 404s, and
   405s for mutating methods.

## Running

```bash
# create venv and install deps
python -m venv env1
source env1/bin/activate
pip install -r requirements.txt

# initialize DB and run server
flask --app app init-db
flask --app app run -p 8000

# run tests
python -m pytest
```
