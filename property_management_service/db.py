import os
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Always load .env from the service directory
load_dotenv(dotenv_path=Path(__file__).parent / ".env")
DATABASE_URL = os.getenv("DATABASE_URL")
print("Loaded DATABASE_URL:", DATABASE_URL)

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
