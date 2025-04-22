# Development Setup

- cd into docker-env-dev and run `docker compose up -d`
- open vscode and connect to app container. Once in the container, open the `/app` folder
- create virtual python env `python -m venv venv`
- install packages `pip install -r requirements.txt`

# Apply migrations

- set `DATABASE_URL` env variable
    - `export DATABASE_URL=DATABASE_URL=postgresql://postgres:postgres@db/waste-management-service`
- run `bash scripts/applyPendingMigrations.sh` from the root folder in the container (folder where run.py file exists)
    - This will apply all pending migrations to the database
    - The script will also create a new database if it does not exist

## Test the app

- run `bash scripts/runTests.sh` from the root folder in the container (folder where run.py file exists)
    - Tests are run using sqlite

## Run the app

- run `bash scripts/runApp.sh` from the root folder in the container (folder where run.py file exists)

### OpenAPI and Swagger UI access

- swagger ui can be accessed at `http://localhost:8001/docs` once the app is running.
- the full OpenAPI spec can be found at `http://localhost:8001/openapi.json` 

