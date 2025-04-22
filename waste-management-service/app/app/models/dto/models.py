import datetime
from pydantic import BaseModel


class CreateMissedWastePickupDto(BaseModel):
    """DTO for creating a missed waste pickup."""

    description: str
    date: str
    address: str
    userId: str


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
