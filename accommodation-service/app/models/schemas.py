from pydantic import BaseModel
from typing import List, Optional

class AccommodationImageBase(BaseModel):
    document_id: int
    image_url: str

class AccommodationImageCreate(AccommodationImageBase):
    pass

class AccommodationImage(AccommodationImageBase):
    id: int
    accommodation_id: int
    
    class Config:
        orm_mode = True

class ReviewBase(BaseModel):
    rating: float
    comment: str

class ReviewCreate(ReviewBase):
    user_id: int

class Review(ReviewBase):
    id: int
    accommodation_id: int
    user_id: int
    
    class Config:
        orm_mode = True

class AccommodationBase(BaseModel):
    name: str
    description: str
    location: str
    website_url: Optional[str] = None
    mobile: Optional[str] = None
    telephone: Optional[str] = None
    email: Optional[str] = None

class AccommodationCreate(AccommodationBase):
    pass

class Accommodation(AccommodationBase):
    id: int
    images: List[AccommodationImage] = []
    
    class Config:
        orm_mode = True

class AccommodationDetail(Accommodation):
    reviews: List[Review] = []
    
    class Config:
        orm_mode = True 