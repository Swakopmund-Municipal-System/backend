import os
import logging
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select
from dotenv import load_dotenv
from models import Base, RestaurantDB, ReviewDB
from sqlalchemy.orm import selectinload
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
DATABASE_URL = os.getenv("DATABASE_URL")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
PORT = int(os.getenv("PORT", "8002"))
HOST = os.getenv("HOST", "0.0.0.0")

# Database setup
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Swakopmund Restaurant Service",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Review(BaseModel):
    id: int
    restaurant_id: int
    user_id: int
    rating: float
    comment: str
    created_at: datetime
    class Config:
        from_attributes = True

class RestaurantCreate(BaseModel):
    name: str
    description: str
    address: str
    phone: Optional[str] = None
    website: Optional[str] = None
    cuisine: Optional[str] = None
    price_range: Optional[str] = None
    hours: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    image_url: Optional[str] = None
    is_featured: bool = False
    rating: float = 0

class Restaurant(BaseModel):
    id: int
    name: str
    description: str
    address: str
    phone: Optional[str] = None
    website: Optional[str] = None
    cuisine: Optional[str] = None
    price_range: Optional[str] = None
    hours: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    image_url: Optional[str] = None
    is_featured: bool = False
    rating: float
    reviews: List[Review] = []
    class Config:
        from_attributes = True

# Dependency
async def get_db():
    async with async_session() as session:
        yield session

# Authentication middleware
async def verify_auth(
    x_api_key: str = Header(None),
    x_resource: str = Header(None),
    x_sub_resource: str = Header(None),
    authorization: str = Header(None)
):
    if not x_api_key or not x_resource:
        raise HTTPException(status_code=401, detail="Missing required headers")
    
    # For anonymous endpoints, we only need to verify the API key
    if x_sub_resource == "fetch-restaurants":
        return True
        
    # For authenticated endpoints, we need both API key and user token
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization token")
        
    # Verify with auth service
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{AUTH_SERVICE_URL}/api/auth/verify",
                headers={
                    "x-api-key": x_api_key,
                    "x-resource": x_resource,
                    "x-sub-resource": x_sub_resource,
                    "authorization": authorization
                }
            )
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid authentication")
            return True
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))

# Initialize database tables
async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise

# Add startup event
@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/", response_model=List[Restaurant])
async def get_restaurants(
    name: Optional[str] = None,
    cuisine: Optional[str] = None,
    price_range: Optional[str] = None,
    is_featured: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    x_api_key: str = Header(None),
    x_resource: str = Header(None)
):
    # Basic API key validation for anonymous access
    if not x_api_key or not x_resource:
        raise HTTPException(status_code=401, detail="Missing required headers")
    
    query = select(RestaurantDB).options(selectinload(RestaurantDB.reviews))
    if name:
        query = query.where(RestaurantDB.name.ilike(f"%{name}%"))
    if cuisine:
        query = query.where(RestaurantDB.cuisine.ilike(f"%{cuisine}%"))
    if price_range:
        query = query.where(RestaurantDB.price_range == price_range)
    if is_featured is not None:
        query = query.where(RestaurantDB.is_featured == is_featured)
    result = await db.execute(query)
    return result.scalars().all()

@app.get("/featured", response_model=List[Restaurant])
async def get_featured_restaurants(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RestaurantDB).where(RestaurantDB.is_featured == True).options(selectinload(RestaurantDB.reviews)))
    return result.scalars().all()

@app.post("/", response_model=Restaurant, status_code=201)
async def create_restaurant(
    restaurant: RestaurantCreate, 
    db: AsyncSession = Depends(get_db)
):
    try:
        logger.info(f"Creating new restaurant: {restaurant.name}")
        new_restaurant = RestaurantDB(
            name=restaurant.name,
            description=restaurant.description,
            address=restaurant.address,
            phone=restaurant.phone,
            website=restaurant.website,
            cuisine=restaurant.cuisine,
            price_range=restaurant.price_range,
            hours=restaurant.hours,
            latitude=restaurant.latitude,
            longitude=restaurant.longitude,
            image_url=restaurant.image_url,
            is_featured=restaurant.is_featured,
            rating=restaurant.rating
        )
        db.add(new_restaurant)
        await db.commit()
        await db.refresh(new_restaurant)
        
        # Explicitly load the reviews relationship
        await db.refresh(new_restaurant, ["reviews"])
        
        logger.info(f"Successfully created restaurant with ID: {new_restaurant.id}")
        return new_restaurant
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating restaurant: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating restaurant: {str(e)}")

@app.put("/{restaurant_id}", response_model=Restaurant)
async def update_restaurant(restaurant_id: int, restaurant: Restaurant, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RestaurantDB).where(RestaurantDB.id == restaurant_id))
    restaurant_db = result.scalar_one_or_none()
    if not restaurant_db:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    restaurant_db.name = restaurant.name
    restaurant_db.description = restaurant.description
    restaurant_db.address = restaurant.address
    restaurant_db.phone = restaurant.phone
    restaurant_db.website = restaurant.website
    restaurant_db.cuisine = restaurant.cuisine
    restaurant_db.price_range = restaurant.price_range
    restaurant_db.hours = restaurant.hours
    restaurant_db.latitude = restaurant.latitude
    restaurant_db.longitude = restaurant.longitude
    restaurant_db.image_url = restaurant.image_url
    restaurant_db.is_featured = restaurant.is_featured
    restaurant_db.rating = restaurant.rating
    await db.commit()
    await db.refresh(restaurant_db)
    return restaurant_db

@app.delete("/{restaurant_id}", status_code=204)
async def delete_restaurant(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RestaurantDB).where(RestaurantDB.id == restaurant_id))
    restaurant_db = result.scalar_one_or_none()
    if not restaurant_db:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    await db.delete(restaurant_db)
    await db.commit()
    return None

@app.get("/{restaurant_id}", response_model=Restaurant)
async def get_restaurant_details(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RestaurantDB).where(RestaurantDB.id == restaurant_id).options(selectinload(RestaurantDB.reviews)))
    restaurant = result.scalar_one_or_none()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

@app.post("/{restaurant_id}/reviews", status_code=200)
async def add_review(
    restaurant_id: int,
    review: Review,
    db: AsyncSession = Depends(get_db),
    _: bool = Depends(verify_auth)
):
    # Check restaurant exists
    result = await db.execute(select(RestaurantDB).where(RestaurantDB.id == restaurant_id).options(selectinload(RestaurantDB.reviews)))
    restaurant = result.scalar_one_or_none()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    # Add review
    new_review = ReviewDB(
        restaurant_id=restaurant_id,
        user_id=review.user_id,
        rating=review.rating,
        comment=review.comment,
        created_at=datetime.now()
    )
    db.add(new_review)
    await db.flush()  # Get the review in session
    # Update restaurant rating
    restaurant.reviews.append(new_review)
    restaurant.rating = sum(r.rating for r in restaurant.reviews) / len(restaurant.reviews)
    await db.commit()
    return {"message": "Review added successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT) 