from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import accommodation
from app.models.accommodation import Base
from app.database.database import engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Accommodation API Service",
    description="API service for accommodation options in Swakopmund",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(accommodation.router)

@app.get("/")
def read_root():
    return {
        "service": "Accommodation API Service",
        "version": "1.0.0",
        "description": "Provides information about accommodation options in Swakopmund"
    } 