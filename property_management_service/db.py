import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Build DATABASE_URL from environment variables (passed from Docker Compose)
DATABASE = os.getenv("DATABASE", "property_db")
USER = os.getenv("USER", "property_user")
PASSWORD = os.getenv("PASSWORD", "property_password")
HOST = os.getenv("HOST", "property_database")
PORT = os.getenv("PORT", "5432")

DATABASE_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
print("Loaded DATABASE_URL:", DATABASE_URL)
print("Environment variables:")
print(f"DATABASE: {DATABASE}")
print(f"USER: {USER}")
print(f"PASSWORD: {PASSWORD}")
print(f"HOST: {HOST}")
print(f"PORT: {PORT}")

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
