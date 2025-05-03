from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from sqlalchemy.exc import NoResultFound
from property_management_service.models import Property as PropertyModel, PropertyValuation as ValuationModel, PermitApplication as PermitModel, PermitStatusEnum
from property_management_service.db import get_db
from property_management_service.crud import get_property_by_id, get_property_valuations, create_permit_application, get_permit_status
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(
    title="Swakopmund Property & Land Management Service",
    description="Manage and provide access to property valuation records, building control, and zoning regulations",
    version="1.0.0"
)

class PermitStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    IN_REVIEW = "in_review"

class Property(BaseModel):
    id: int
    address: str
    owner_name: str
    property_type: str
    size: float
    zoning: str
    last_valuation_date: datetime

    class Config:
        orm_mode = True

class PropertyValuation(BaseModel):
    id: int
    property_id: int
    value: float
    valuation_date: datetime
    assessed_by: str
    notes: Optional[str]

    class Config:
        orm_mode = True

class PermitApplication(BaseModel):
    id: int
    property_id: int
    applicant_name: str
    application_type: str
    description: str
    status: PermitStatus
    submission_date: datetime
    development_plans: Optional[str]

    class Config:
        orm_mode = True

@app.post("/properties", response_model=Property)
async def create_property(property: Property, db: AsyncSession = Depends(get_db)):
    db_property = PropertyModel(
        id=property.id,
        address=property.address,
        owner_name=property.owner_name,
        property_type=property.property_type,
        size=property.size,
        zoning=property.zoning,
        last_valuation_date=property.last_valuation_date
    )
    db.add(db_property)
    await db.commit()
    await db.refresh(db_property)
    return db_property

@app.get("/properties/{property_id}", response_model=Property)
async def get_property_details(property_id: int, db=Depends(get_db)):
    try:
        property = await get_property_by_id(db, property_id)
        return property
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Property not found")

@app.get("/properties/valuations/{property_id}", response_model=List[PropertyValuation])
async def get_property_valuations_endpoint(property_id: int, db=Depends(get_db)):
    vals = await get_property_valuations(db, property_id)
    return vals

@app.post("/properties/apply-permit", response_model=PermitApplication)
async def apply_permit(
    property_id: int,
    applicant_name: str,
    application_type: str,
    description: str,
    development_plans: Optional[str] = None,
    db=Depends(get_db)
):
    permit_data = {
        "property_id": property_id,
        "applicant_name": applicant_name,
        "application_type": application_type,
        "description": description,
        "status": PermitStatusEnum.PENDING,
        "submission_date": datetime.now(),
        "development_plans": development_plans or ""
    }
    permit = await create_permit_application(db, permit_data)
    return permit

@app.get("/properties/permit-status/{permit_id}", response_model=PermitApplication)
async def get_permit_status_endpoint(permit_id: int, db=Depends(get_db)):
    try:
        permit = await get_permit_status(db, permit_id)
        return permit
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Permit not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)