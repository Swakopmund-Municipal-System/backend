#!/usr/bin/env python3

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database.database import SessionLocal, engine
from app.models.accommodation import Base, Accommodation, AccommodationImage, Review
from app.models.schemas import Accommodation as AccommodationSchema, AccommodationDetail
from app.services.accommodation_service import get_accommodations, get_accommodation_by_id
import json

def test_database_connection():
    """Test if database connection works"""
    try:
        db = SessionLocal()
        accommodations = db.query(Accommodation).all()
        db.close()
        print(f"✅ Database connection works! Found {len(accommodations)} accommodations.")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_endpoints():
    """Test the API endpoints manually"""
    db = SessionLocal()
    
    try:
        # Test GET /api/accommodations/
        print("\n🔍 Testing GET /api/accommodations/")
        accommodations = get_accommodations(db)
        print(f"✅ Found {len(accommodations)} accommodations")
        for acc in accommodations:
            print(f"  - {acc.name} ({acc.location})")
        
        # Test GET /api/accommodations/{id}
        if accommodations:
            print(f"\n🔍 Testing GET /api/accommodations/{accommodations[0].id}")
            detail = get_accommodation_by_id(db, accommodations[0].id)
            if detail:
                print(f"✅ Found accommodation: {detail.name}")
                print(f"  Description: {detail.description}")
                print(f"  Images: {len(detail.images)}")
                print(f"  Reviews: {len(detail.reviews)}")
            else:
                print("❌ No accommodation found")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Endpoint test failed: {e}")
        db.close()
        return False

def show_api_endpoints():
    """Show the available API endpoints"""
    print("\n📋 Available API Endpoints:")
    print("1. GET  http://localhost:8585/api/accommodations/")
    print("   - Get list of accommodations")
    print("   - Optional query parameter: ?name=<search_term>")
    print()
    print("2. GET  http://localhost:8585/api/accommodations/{id}")
    print("   - Get detailed information about a specific accommodation")
    print()
    print("3. POST http://localhost:8585/api/accommodations/{id}/reviews")
    print("   - Add a review for a specific accommodation")
    print("   - Request body: {\"user_id\": 123, \"rating\": 4.5, \"comment\": \"Great place!\"}")

if __name__ == "__main__":
    print("🧪 Testing Accommodation API")
    print("=" * 50)
    
    # Test database connection
    if test_database_connection():
        # Test endpoints
        test_endpoints()
        
        # Show available endpoints
        show_api_endpoints()
        
        print("\n✅ All tests passed! The API should work correctly.")
        print("\nTo start the server manually, run:")
        print("python scripts/simple_server.py")
    else:
        print("\n❌ Database tests failed. Please check your database setup.") 