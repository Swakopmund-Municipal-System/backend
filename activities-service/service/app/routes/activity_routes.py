from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List, Optional

from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.dto.models import ActivityCreateDTO, ActivityEditDTO
from app.services.activities_service import (
    create_activity,
    delete_activity_by_id,
    edit_activity,
    get_activity_by_id,
    search_activities,
    search_activities_by_location,
)
from app.services.auth_service import (
    RESOURCE_NAME,
    authenticate_request,
    authenticate_request_with_user,
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
    auth_data: dict = Depends(
        authenticate_request_with_user(
            RESOURCE_NAME, "modify-activities", "create-activity"
        )
    ),
):
    print("auth data for create", auth_data)

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

    (created_activity_id, status_code, err_message) = create_activity(
        db, activity_data, auth_data["user"]["user"]["id"]
    )
    if status_code != 201:
        raise HTTPException(status_code=status_code, detail=err_message)

    return JSONResponse(
        status_code=201,
        content=created_activity_id,
    )


@router.get(
    "/search",
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
    categories: Optional[str] = None,
    db: Session = Depends(get_db),
    auth_data: dict = Depends(
        authenticate_request(RESOURCE_NAME, "fetch-activities", "get-activities")
    ),
):
    try:
        return search_activities(
            db, search_term, sort_field, sort_order, limit, page, categories
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/search/location",
    responses={
        201: {"description": "search successful."},
        400: {"description": "Invalid input data."},
        500: {"description": "Internal server error."},
    },
)
async def get_activities_by_location(
    latitude: float,
    longitude: float,
    radius: int = 1000,
    search_term: str = "",
    categories: Optional[str] = None,
    db: Session = Depends(get_db),
    auth_data: dict = Depends(
        authenticate_request(
            RESOURCE_NAME, "fetch-activities", "get-activities-by-location"
        )
    ),
):
    try:
        return search_activities_by_location(
            db, latitude, longitude, radius, search_term, categories
        )
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
    auth_data: dict = Depends(
        authenticate_request_with_user(
            RESOURCE_NAME, "modify-activities", "edit-activity"
        )
    ),
):
    (success, status_code, err_message) = edit_activity(
        db, data, auth_data["user"]["user"]["id"]
    )
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=err_message)

    return JSONResponse(
        status_code=200,
        content={"message": "Activity updated successfully."},
    )


@router.delete(
    "/{activity_id}",
    responses={
        200: {"description": "Activity deleted successfully."},
        404: {"description": "Activity not found."},
        500: {"description": "Internal server error."},
    },
)
async def delete_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    auth_data: dict = Depends(
        authenticate_request(RESOURCE_NAME, "modify-activities", "delete-activity")
    ),
):
    (success, status_code, err_message) = delete_activity_by_id(db, activity_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=err_message)

    return JSONResponse(
        status_code=200,
        content={"message": "Activity deleted successfully."},
    )


@router.get(
    "/{activity_id}",
    responses={
        200: {"description": "Activity retrieved successfully."},
        404: {"description": "Activity not found."},
        500: {"description": "Internal server error."},
    },
)
async def get_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    auth_data: dict = Depends(
        authenticate_request(RESOURCE_NAME, "fetch-activities", "get-activity")
    ),
):
    (activity_data, status_code, err_message) = get_activity_by_id(db, activity_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=err_message)

    return JSONResponse(
        status_code=200,
        content=activity_data.model_dump_json(),
    )
