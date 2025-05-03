import asyncio
from property_management_service.db import engine
from property_management_service.models import Base

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Property DB initialized.")

if __name__ == "__main__":
    asyncio.run(init_db())
