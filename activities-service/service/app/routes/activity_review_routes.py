from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List, Optional

from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.dto.models import ActivityCreateDTO, ActivityEditDTO, CreateReviewDTO
from app.services.activity_reviews_service import (
    create_activity_review,
    delete_activity_review_by_id,
    search_activity_reviews,
)
from app.services.auth_service import (
    RESOURCE_NAME,
    authenticate_request,
    authenticate_request_with_user,
    get_auth_headers,
)

router = APIRouter()


@router.post(
    "/",
    responses={
        201: {"description": "Review created successfully."},
        404: {"description": "Activity not found"},
        400: {"description": "Invalid input data."},
        500: {"description": "Internal server error."},
    },
)
async def create_new_activity_review(
    data: CreateReviewDTO,
    db: Session = Depends(get_db),
    auth_data: dict = Depends(
        authenticate_request_with_user(
            RESOURCE_NAME, "review-activities", "create-review"
        )
    ),
):
    (created_review_id, status_code, err_message) = create_activity_review(
        db, data, auth_data["user"]["user"]["id"]
    )
    if status_code != 201:
        raise HTTPException(status_code=status_code, detail=err_message)

    return JSONResponse(
        status_code=201,
        content=created_review_id,
    )


@router.get(
    "/",
    responses={
        201: {"description": "Review created successfully."},
        400: {"description": "Invalid input data."},
        500: {"description": "Internal server error."},
    },
)
async def get_reviews(
    search_term: str = "",
    sort_field: str = "id",
    sort_order: str = "desc",
    limit: int = 10,
    page: int = 1,
    activity_id: int = 0,
    db: Session = Depends(get_db),
    auth_data: dict = Depends(
        authenticate_request(RESOURCE_NAME, "review-activities", "create-review")
    ),
):
    try:
        return search_activity_reviews(
            db, search_term, sort_field, sort_order, limit, page, activity_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/{review_id}",
    responses={
        200: {"description": "Review deleted successfully."},
        404: {"description": "Review not found."},
        500: {"description": "Internal server error."},
    },
)
async def delete_activity_review(
    review_id: int,
    db: Session = Depends(get_db),
    auth_data: dict = Depends(
        authenticate_request(RESOURCE_NAME, "review-activities", "delete-review")
    ),
):
    (success, status_code, err_message) = delete_activity_review_by_id(db, review_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=err_message)

    return JSONResponse(
        status_code=200,
        content={"message": "Activity deleted successfully."},
    )
