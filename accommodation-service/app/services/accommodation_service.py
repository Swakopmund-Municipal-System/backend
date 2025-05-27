from sqlalchemy.orm import Session
from app.models.accommodation import Accommodation, AccommodationImage, Review
from app.models.schemas import AccommodationCreate, ReviewCreate
from typing import List, Optional

def get_accommodations(db: Session, name: Optional[str] = None):
    query = db.query(Accommodation)
    if name:
        query = query.filter(Accommodation.name.ilike(f"%{name}%"))
    return query.all()

def get_accommodation_by_id(db: Session, accommodation_id: int):
    return db.query(Accommodation).filter(Accommodation.id == accommodation_id).first()

def create_accommodation(db: Session, accommodation: AccommodationCreate):
    db_accommodation = Accommodation(**accommodation.dict())
    db.add(db_accommodation)
    db.commit()
    db.refresh(db_accommodation)
    return db_accommodation

def add_accommodation_image(db: Session, accommodation_id: int, document_id: int, image_url: str):
    db_image = AccommodationImage(
        accommodation_id=accommodation_id,
        document_id=document_id,
        image_url=image_url
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def add_review(db: Session, accommodation_id: int, review: ReviewCreate):
    db_review = Review(
        accommodation_id=accommodation_id,
        user_id=review.user_id,
        rating=review.rating,
        comment=review.comment
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review 