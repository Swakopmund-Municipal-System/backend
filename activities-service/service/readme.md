
# Development setup

## Prerequisites
- docker & docker compose installed
- vscode installed

## Creating the dev environment
- cd into `docker-env-dev` folder
- run `docker-compose up -d` to start the dev environment
   - this will create a development python container, a postgres database container, and a pgadmin container
- run `docker-compose exec app python manage.py migrate` to create the database tables
- in vscode, open the `docker-env-dev-app-1` container in the remote explorer
- open the `/app` folder in the container
- create a new python virtual environment in the container using `python -m venv .venv` (or use the python extension to create a new virtual environment)
- activate the virtual environment using `source .venv/bin/activate` (or use the python extension to activate the virtual environment)
- install the required packages using `pip install -r requirements.txt` (or use the python extension to install the required packages)

## Setting up the database  (done inside the development container)
- set the DATABASE_URL environment: `export DATABASE_URL=postgresql://postgres:postgres@db/activities-service` 
   - this uses the default credentials for the postgres database container. Change if necessary.
- in the root folder (`/app`), run `bash scripts/applyPendingMigrations.sh` to apply any pending migrations to the database

## Running the application
- in the root folder (`/app`), run `bash scripts/runApp.sh` to start the application


## Running the tests
- the tests require an instance of postgres to be running. In this case we can use the development postgres container created above.
   - In github actions, an instance of postgres must be created for the tests to run.
- in the root folder (`/app`), run `bash scripts/runTests.sh` to run the tests