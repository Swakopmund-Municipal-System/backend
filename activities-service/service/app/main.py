from typing import List
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session

from app.database import Base, get_engine
from app.routes import activity_image_routes, activity_review_routes, activity_routes

import os

if not os.path.exists("uploads"):
    os.makedirs("uploads")


Base.metadata.create_all(bind=get_engine())

app = FastAPI(
    title="Activities Service",
    description="Activities Management Service",
    version="1.0.0",
    openapi_tags=[],
)

app.include_router(activity_routes.router, prefix="/api/activities", tags=[])
app.include_router(
    activity_image_routes.router, prefix="/api/activities/images", tags=[]
)
app.include_router(
    activity_review_routes.router, prefix="/api/activities/reviews", tags=[]
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "X-API-KEY": {"type": "apiKey", "in": "header", "name": "X-API-KEY"},
        "Authorization": {"type": "apiKey", "in": "header", "name": "Authorization"},
    }

    openapi_schema["security"] = [
        {"X-API-KEY": []},
        {"Authorization": []},
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
