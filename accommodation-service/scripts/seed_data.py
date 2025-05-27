#!/usr/bin/env python3

"""
Script to seed the database with sample accommodation data.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database.database import SessionLocal, engine
from app.models.accommodation import Base, Accommodation, AccommodationImage, Review

def create_sample_data():
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_accommodations = db.query(Accommodation).count()
        if existing_accommodations > 0:
            print(f"✅ Database already has {existing_accommodations} accommodations. Skipping seed.")
            return
        
        # Create sample accommodations
        accommodations_data = [
            {
                "name": "Swakopmund Hotel & Entertainment Centre",
                "description": "Located in the heart of Swakopmund, this historic hotel offers luxury accommodation with easy access to the beach and city attractions.",
                "location": "2 Theo-Ben Gurirab Ave, Swakopmund",
                "website_url": "https://swakopmund-hotel.com",
                "mobile": "+264 64 410 200",
                "telephone": "+264 64 410 200",
                "email": "reservations@swakopmund-hotel.com"
            },
            {
                "name": "The Delight Swakopmund",
                "description": "A boutique hotel offering modern amenities and personalized service in the center of Swakopmund.",
                "location": "1 Libertina Amathila Ave, Swakopmund",
                "website_url": "https://thedelight.com.na",
                "mobile": "+264 64 463 200",
                "telephone": "+264 64 463 200",
                "email": "info@thedelight.com.na"
            },
            {
                "name": "Beach Lodge Swakopmund",
                "description": "Oceanfront accommodation with stunning sea views and direct beach access.",
                "location": "Strand Street, Swakopmund",
                "website_url": "https://beachlodge-swakopmund.com",
                "mobile": "+264 64 400 844",
                "telephone": "+264 64 400 844",
                "email": "reservations@beachlodge-swakopmund.com"
            }
        ]
        
        # Create accommodations
        accommodations = []
        for i, acc_data in enumerate(accommodations_data, 1):
            accommodation = Accommodation(**acc_data)
            db.add(accommodation)
            db.flush()  # Get the ID
            accommodations.append(accommodation)
            
            # Add sample images for each accommodation
            for j in range(2):  # 2 images per accommodation
                image = AccommodationImage(
                    document_id=f"img_{accommodation.id}_{j+1}",
                    image_url=f"https://example.com/images/accommodation_{accommodation.id}_image_{j+1}.jpg",
                    accommodation_id=accommodation.id
                )
                db.add(image)
            
            # Add sample reviews
            reviews_data = [
                {"user_id": 101, "rating": 4.5, "comment": "Great location and friendly staff!"},
                {"user_id": 102, "rating": 5.0, "comment": "Excellent accommodation, highly recommended!"},
                {"user_id": 103, "rating": 4.0, "comment": "Good value for money, clean rooms."}
            ]
            
            for review_data in reviews_data:
                review = Review(
                    **review_data,
                    accommodation_id=accommodation.id
                )
                db.add(review)
        
        # Commit all changes
        db.commit()
        print(f"✅ Successfully created {len(accommodations)} accommodations with images and reviews!")
        
        # Display created data
        for acc in accommodations:
            print(f"  📍 {acc.name} (ID: {acc.id})")
            print(f"     Location: {acc.location}")
            print(f"     Images: {len(acc.images)}")
            print(f"     Reviews: {len(acc.reviews)}")
            print()
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🌱 Seeding database with sample accommodation data...")
    print("=" * 60)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created/verified")
    
    # Create sample data
    create_sample_data()
    
    print("🎉 Database seeding completed!") 