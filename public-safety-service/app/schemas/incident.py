"""
Pydantic schemas for incident operations
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date, datetime
from enum import Enum


class IncidentStatus(str, Enum):
    """Enum for incident status values"""
    REPORTED = "REPORTED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class IncidentReportRequest(BaseModel):
    """Schema for reporting a new incident"""
    user_id: int = Field(..., gt=0, description="ID of the user reporting the incident")
    location: str = Field(..., min_length=1, max_length=255, description="General location of the incident")
    address: str = Field(..., min_length=1, max_length=255, description="Specific address of the incident")
    description: str = Field(..., min_length=10, description="Detailed description of the incident")
    
    @validator('location', 'address')
    def validate_location_fields(cls, v):
        if not v.strip():
            raise ValueError('Location and address cannot be empty')
        return v.strip()


class IncidentStatusUpdate(BaseModel):
    """Schema for updating incident status"""
    status: IncidentStatus = Field(..., description="New status for the incident")


class IncidentResponse(BaseModel):
    """Schema for incident response"""
    id: int
    description: str
    date: date
    location: str
    address: str
    status: str
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class IncidentListResponse(BaseModel):
    """Schema for paginated incident list response"""
    incidents: list[IncidentResponse]
    total: int
    page: int
    size: int
    total_pages: int


class ApiResponse(BaseModel):
    """Generic API response schema"""
    success: bool
    message: str
    data: Optional[dict] = None 