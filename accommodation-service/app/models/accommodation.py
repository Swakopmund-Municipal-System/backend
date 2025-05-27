from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Accommodation(Base):
    __tablename__ = "accommodations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    location = Column(String)
    website_url = Column(Text)
    mobile = Column(String)
    telephone = Column(String)
    email = Column(String)
    
    images = relationship("AccommodationImage", back_populates="accommodation")
    reviews = relationship("Review", back_populates="accommodation")

class AccommodationImage(Base):
    __tablename__ = "accommodation_images"
    
    id = Column(Integer, primary_key=True, index=True)
    accommodation_id = Column(Integer, ForeignKey("accommodations.id"))
    document_id = Column(Integer)
    image_url = Column(String)
    
    accommodation = relationship("Accommodation", back_populates="images")

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    accommodation_id = Column(Integer, ForeignKey("accommodations.id"))
    user_id = Column(Integer)
    rating = Column(Float)
    comment = Column(Text)
    
    accommodation = relationship("Accommodation", back_populates="reviews") 