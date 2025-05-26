from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, field_validator
from datetime import datetime
from enum import Enum
from sqlalchemy.exc import NoResultFound
from models import Property as PropertyModel, PropertyValuation as ValuationModel, PermitApplication as PermitModel, PermitStatusEnum
from db import get_db
from crud import get_property_by_id, get_property_valuations, create_permit_application, get_permit_status
from sqlalchemy.ext.asyncio import AsyncSession
from auth import get_current_user, get_current_user_optional

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
    id: Optional[int] = None
    address: str
    owner_name: str
    property_type: str
    size: float
    zoning: str
    last_valuation_date: datetime

    @field_validator('last_valuation_date')
    @classmethod
    def convert_datetime(cls, v):
        if v and v.tzinfo is not None:
            # Convert timezone-aware datetime to naive datetime
            return v.replace(tzinfo=None)
        return v

    class Config:
        from_attributes = True

class PropertyValuation(BaseModel):
    id: Optional[int] = None
    property_id: int
    value: float
    valuation_date: datetime
    assessed_by: str
    notes: Optional[str]

    @field_validator('valuation_date')
    @classmethod
    def convert_datetime(cls, v):
        if v and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v

    class Config:
        from_attributes = True

class PermitApplication(BaseModel):
    id: Optional[int] = None
    property_id: int
    applicant_name: str
    application_type: str
    description: str
    status: PermitStatus
    submission_date: Optional[datetime] = None
    development_plans: Optional[str]

    @field_validator('submission_date')
    @classmethod
    def convert_datetime(cls, v):
        if v and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v

    class Config:
        from_attributes = True

@app.post("/properties", response_model=Property)
async def create_property(
    property: Property, 
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Create a new property. Requires authentication.
    Allowed roles: Property Developer (write), Planning Department (admin), Building Inspector (admin)
    """
    db_property = PropertyModel(
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
async def get_property_details(
    property_id: int, 
    db=Depends(get_db),
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user_optional)
):
    """
    Get property details. Supports anonymous access.
    Allowed roles: Anonymous, Resident (read), Tourist (read), Property Developer (read), Planning Department (read), Building Inspector (read)
    """
    try:
        property = await get_property_by_id(db, property_id)
        if not property:
            raise HTTPException(status_code=404, detail="Property not found")
        return property
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Property not found")

@app.get("/properties/valuations/{property_id}", response_model=List[PropertyValuation])
async def get_property_valuations_endpoint(
    property_id: int, 
    db=Depends(get_db),
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user_optional)
):
    """
    Get property valuations. Supports anonymous access.
    Allowed roles: Anonymous, Resident (read), Tourist (read), Property Developer (read), Planning Department (read), Building Inspector (read)
    """
    vals = await get_property_valuations(db, property_id)
    return vals

@app.post("/properties/valuations", response_model=PropertyValuation)
async def create_property_valuation(
    valuation: PropertyValuation, 
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Create a property valuation. Requires authentication.
    Allowed roles: Property Developer (write), Planning Department (admin), Building Inspector (admin)
    """
    # First check if the property exists
    property_exists = await get_property_by_id(db, valuation.property_id)
    if not property_exists:
        raise HTTPException(status_code=404, detail="Property not found")
    
    db_valuation = ValuationModel(
        property_id=valuation.property_id,
        value=valuation.value,
        valuation_date=valuation.valuation_date,
        assessed_by=valuation.assessed_by,
        notes=valuation.notes
    )
    db.add(db_valuation)
    await db.commit()
    await db.refresh(db_valuation)
    return db_valuation

@app.post("/properties/apply-permit", response_model=PermitApplication)
async def apply_permit(
    property_id: int,
    applicant_name: str,
    application_type: str,
    description: str,
    development_plans: Optional[str] = None,
    db=Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Apply for a building permit. Requires authentication.
    Allowed roles: Property Developer (write), Planning Department (admin), Building Inspector (admin)
    """
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
async def get_permit_status_endpoint(
    permit_id: int, 
    db=Depends(get_db),
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user_optional)
):
    """
    Get permit status. Supports anonymous access.
    Allowed roles: Anonymous, Resident (read), Tourist (read), Property Developer (read), Planning Department (read), Building Inspector (read)
    """
    try:
        permit = await get_permit_status(db, permit_id)
        if not permit:
            raise HTTPException(status_code=404, detail="Permit not found")
        return permit
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Permit not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)