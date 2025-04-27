import os
from sqlalchemy import create_engine
from models import Base
from dotenv import load_dotenv

# Explicitly load the .env file from the current directory
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path, override=True)
DATABASE_URL = os.getenv("DATABASE_URL")
print("Loaded DATABASE_URL:", DATABASE_URL)  # Debug print

# Convert the asyncpg URL to a psycopg2 URL for sync operations
sync_url = DATABASE_URL.replace("asyncpg", "psycopg2")
print("Sync URL used:", sync_url)  # Debug print

engine = create_engine(sync_url)

def create_tables():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables()