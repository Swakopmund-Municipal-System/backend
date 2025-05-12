from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import crud
from app.database import Base, SessionLocal, get_engine
from app.models.dto.models import (
    CreateMissedWastePickupDto,
    MissedWastePickupSearchResultDto,
    UpdateMissedWastePickupStatusDto,
)
from app.services.auth_service import RESOURCE_NAME, authenticate_request_with_user

Base.metadata.create_all(bind=get_engine())

app = FastAPI(
    title="Waste management service",
    description="Manages waste management operations",
    version="1.0.0",
    openapi_tags=[],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/api/waste-management/missed_waste_pickups/",
    responses={
        201: {"description": "Missed waste pickup created successfully."},
        400: {"description": "Invalid input data."},
        500: {"description": "Internal server error."},
    },
)
def create_missed_waste_pickup(
    data: CreateMissedWastePickupDto,
    db: Session = Depends(get_db),
    auth_data: dict = Depends(
        authenticate_request_with_user(RESOURCE_NAME, "missed-waste-pickups", "create")
    ),
):
    (record, status_code, err_message) = crud.create_missed_waste_pickup(
        db, data, auth_data["user"]["user"]["id"]
    )
    if status_code != 201:
        raise HTTPException(status_code=status_code, detail=err_message)

    return JSONResponse(
        status_code=201,
        content={},
    )


@app.get(
    "/api/waste-management/missed_waste_pickups",
    response_model=List[MissedWastePickupSearchResultDto],
    responses={200: {"description": "list of missed waste pickups"}},
)
def get_missed_waste_pickups(
    search_term: str = "",
    sort_field: str = "id",
    sort_order: str = "desc",
    limit: int = 10,
    page: int = 1,
    db: Session = Depends(get_db),
    auth_data: dict = Depends(
        authenticate_request_with_user(RESOURCE_NAME, "missed-waste-pickups", "search")
    ),
):
    results = crud.search_missed_waste_pickups(
        db=db,
        search_term=search_term,
        sort_field=sort_field,
        sort_order=sort_order,
        limit=limit,
        page=page,
    )
    return results


@app.get(
    "/api/waste-management/missed_waste_pickups/{id}",
    response_model=MissedWastePickupSearchResultDto,
    responses={
        200: {"description": "details of missed waste pickup"},
        400: {"description": "Invalid input data."},
        404: {"description": "Missed waste pickup not found."},
    },
)
def get_missed_waste_pickup_details(
    id: int,
    db: Session = Depends(get_db),
    auth_data: dict = Depends(
        authenticate_request_with_user(
            RESOURCE_NAME, "missed-waste-pickups", "get_details"
        )
    ),
):
    if not id:
        raise HTTPException(
            status_code=400, detail="Invalid input data. ID is required."
        )
    if id < 1:
        raise HTTPException(
            status_code=400, detail="Invalid input data. ID must be greater than 0."
        )

    result = crud.get_missed_waste_pickup_details(
        db=db,
        id=id,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Missed waste pickup not found.")

    return result


@app.post(
    "/api/waste-management/missed_waste_pickups/update_status",
    responses={
        200: {"description": "Status updated successfully."},
        400: {"description": "Invalid input data."},
        500: {"description": "Internal server error."},
    },
)
def update_missed_waste_pickup_status(
    data: UpdateMissedWastePickupStatusDto,
    db: Session = Depends(get_db),
    auth_data: dict = Depends(
        authenticate_request_with_user(
            RESOURCE_NAME, "missed-waste-pickups", "update_status"
        )
    ),
):
    (success, status_code, err_message) = crud.update_missed_waste_pickup_status(
        db, data
    )
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=err_message)

    return {}
