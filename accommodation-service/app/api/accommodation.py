from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.database import get_db
from app.models.schemas import Accommodation, AccommodationDetail, ReviewCreate
from app.services import accommodation_service

router = APIRouter(prefix="/api/accommodations", tags=["accommodations"])

@router.get("/", response_model=List[Accommodation])
def get_accommodations(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get list of accommodations, optionally filtered by name
    """
    accommodations = accommodation_service.get_accommodations(db, name)
    return accommodations

@router.get("/{id}", response_model=AccommodationDetail)
def get_accommodation_details(id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific accommodation
    """
    accommodation = accommodation_service.get_accommodation_by_id(db, id)
    if accommodation is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    return accommodation

@router.post("/{id}/reviews", status_code=status.HTTP_200_OK)
def add_review(id: int, review: ReviewCreate, db: Session = Depends(get_db)):
    """
    Add a review for a specific accommodation
    """
    accommodation = accommodation_service.get_accommodation_by_id(db, id)
    if accommodation is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    
    accommodation_service.add_review(db, id, review)
    return {"status": "success", "status_code": 200} 