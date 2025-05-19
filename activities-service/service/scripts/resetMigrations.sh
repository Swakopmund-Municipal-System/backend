ls

rm -rf migrations/versions/*
alembic revision --autogenerate -m "Initial migration"