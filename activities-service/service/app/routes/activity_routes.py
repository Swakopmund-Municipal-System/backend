from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List, Optional

from fastapi.responses import JSONResponse
from pydantic import ValidationError
from pytest import Session

from app.database import get_db
from app.models.dto.models import ActivityCreateDTO, ActivityEditDTO
from app.services.activities_service import (
    create_activity,
    edit_activity,
    search_activities,
)

router = APIRouter()


@router.post(
    "/",
    responses={
        201: {"description": "Activity created successfully."},
        400: {"description": "Invalid input data."},
        500: {"description": "Internal server error."},
    },
)
async def create_new_activity(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    type: int = Form(...),
    files: Optional[List[UploadFile]] = File(None),
    latitude: float = Form(...),
    longitude: float = Form(...),
    address: str = Form(...),
    booking_url: str = Form(...),
    hero_image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):

    try:
        activity_data = ActivityCreateDTO(
            name=name,
            description=description,
            type=type,
            files=files,
            address=address,
            booking_url=booking_url,
            hero_image=hero_image,
            latitude=latitude,
            longitude=longitude,
        )

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())

    (created_activity_id, status_code, err_message) = create_activity(db, activity_data)
    if status_code != 201:
        raise HTTPException(status_code=status_code, detail=err_message)

    return JSONResponse(
        status_code=201,
        content=created_activity_id,
    )


@router.get(
    "/",
    responses={
        201: {"description": "Activity created successfully."},
        400: {"description": "Invalid input data."},
        500: {"description": "Internal server error."},
    },
)
async def get_activities(
    search_term: str = "",
    sort_field: str = "id",
    sort_order: str = "desc",
    limit: int = 10,
    page: int = 1,
    db: Session = Depends(get_db),
):
    try:
        return search_activities(db, search_term, sort_field, sort_order, limit, page)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/edit",
    responses={
        200: {"description": "Activity edited successfully."},
        400: {"description": "Invalid input data."},
        404: {"description": "Activity not found."},
        500: {"description": "Internal server error."},
    },
)
async def update_activity(
    data: ActivityEditDTO,
    db: Session = Depends(get_db),
):
    (success, status_code, err_message) = edit_activity(db, data)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=err_message)

    return JSONResponse(
        status_code=200,
        content={"message": "Activity updated successfully."},
    )
