from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Property, PropertyValuation, PermitApplication

async def get_property_by_id(session: AsyncSession, property_id: int):
    stmt = select(Property).where(Property.id == property_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_property_valuations(session: AsyncSession, property_id: int):
    stmt = select(PropertyValuation).where(PropertyValuation.property_id == property_id)
    result = await session.execute(stmt)
    return result.scalars().all()

async def create_permit_application(session: AsyncSession, permit_data: dict):
    permit = PermitApplication(**permit_data)
    session.add(permit)
    await session.commit()
    await session.refresh(permit)
    return permit

async def get_permit_status(session: AsyncSession, permit_id: int):
    stmt = select(PermitApplication).where(PermitApplication.id == permit_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
