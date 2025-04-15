from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi import UploadFile


class ActivityBase(BaseModel):
    name: str = Field(..., example="Go Carting", min_length=3, max_length=255)
    description: Optional[str] = Field(
        None, example="Fast family fun", min_length=3, max_length=512
    )
    latitude: float
    longitude: float
    type: int
    address: str = Field(
        ..., example="123 Fun St, Fun City", min_length=3, max_length=255
    )
    booking_url: str


class ActivityCreateDTO(ActivityBase):
    hero_image: Optional[UploadFile] = None
    files: Optional[List[UploadFile]] = None


class ActivitySearchResultDTO(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example="Go Carting")
    description: Optional[str] = Field(None, example="Fast family fun")
    address: str = Field(..., example="123 Fun St, Fun City")
    type: int = Field(..., example=1)
    createdAt: str = Field(..., example="2023-10-01T12:00:00Z")
    updatedAt: str = Field(..., example="2023-10-01T12:00:00Z")
    latitude: float = Field(..., example=12.345678)
    longitude: float = Field(..., example=12.345678)
    image_id: int = Field(..., example=1)
    booking_url: str = Field(..., example="https://example.com/booking/go-carting")
