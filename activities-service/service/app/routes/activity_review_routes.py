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
async def create_new_activity(
    data: CreateReviewDTO,
    db: Session = Depends(get_db),
):
    (created_review_id, status_code, err_message) = create_activity_review(db, data)
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
async def get_activities(
    search_term: str = "",
    sort_field: str = "id",
    sort_order: str = "desc",
    limit: int = 10,
    page: int = 1,
    activity_id: int = 0,
    db: Session = Depends(get_db),
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
async def delete_activity(
    review_id: int,
    db: Session = Depends(get_db),
):
    (success, status_code, err_message) = delete_activity_review_by_id(db, review_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=err_message)

    return JSONResponse(
        status_code=200,
        content={"message": "Activity deleted successfully."},
    )
