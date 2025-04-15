from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List, Optional

from pydantic import ValidationError
from pytest import Session

from app.database import get_db
from app.models.dto.models import ActivityCreateDTO
from app.services.activities_service import search_activities

router = APIRouter()


@router.post(
    "/",
    responses={
        201: {"description": "Activity created successfully."},
        400: {"description": "Invalid input data."},
        500: {"description": "Internal server error."},
    },
)
async def create_activity(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    type: int = Form(...),
    files: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db),
):

    try:
        activity_data = ActivityCreateDTO(
            name=name, description=description, type=type, files=files
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())

    return {
        "dto": activity_data.model_dump(exclude={"files"}),
        "filenames": [f.filename for f in files] if files else [],
    }


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
