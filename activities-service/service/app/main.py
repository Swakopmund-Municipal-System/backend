from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import Base, get_engine
from app.routes import activity_image_routes, activity_routes

Base.metadata.create_all(bind=get_engine())

app = FastAPI(
    title="Activities Service",
    description="Activities Management Service",
    version="1.0.0",
    openapi_tags=[],
)


app.include_router(activity_routes.router, prefix="/activities", tags=[])
app.include_router(activity_image_routes.router, prefix="/activities/images", tags=[])
