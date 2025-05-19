import datetime
from pydantic import BaseModel, Field


class CreateMissedWastePickupDto(BaseModel):
    """DTO for creating a missed waste pickup."""

    description: str
    date: str
    address: str


class MissedWastePickupSearchResultDto(BaseModel):
    """DTO for the result of a missed waste pickup search."""

    id: int
    description: str
    date: str
    address: str
    status: int
    userId: str


class UpdateMissedWastePickupStatusDto(BaseModel):
    """DTO for updating the status of a missed waste pickup."""

    id: int
    status: int


class AuthenticatedUserDTO(BaseModel):
    id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")
    email: str = Field(..., example="abc@a.com")
    is_staff: bool = Field(..., example=False)
