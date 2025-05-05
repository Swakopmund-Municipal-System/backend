import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select
from dotenv import load_dotenv
from models import Base, RestaurantDB, ReviewDB
from sqlalchemy.orm import selectinload

# env_path = os.path.join(os.path.dirname(__file__), '.env')
# load_dotenv(dotenv_path=env_path, override=True)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
# engine = create_async_engine(DATABASE_URL, echo=True)
# async_session = async_sessionmaker(engine, expire_on_commit=False)
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Swakopmund Restaurant Service", root_path="/api/restaurants")

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
        orm_mode = True

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
        orm_mode = True

# Dependency
async def get_db():
    async with async_session() as session:
        yield session

@app.get("/", response_model=List[Restaurant])
async def get_restaurants(
    name: Optional[str] = None,
    cuisine: Optional[str] = None,
    price_range: Optional[str] = None,
    is_featured: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
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
async def create_restaurant(restaurant: RestaurantCreate, db: AsyncSession = Depends(get_db)):
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
    return new_restaurant

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
async def add_review(restaurant_id: int, review: Review, db: AsyncSession = Depends(get_db)):
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
    uvicorn.run(app, host="0.0.0.0", port=8002) 