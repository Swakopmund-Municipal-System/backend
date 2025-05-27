"""
Fire department API endpoints for incident management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.core.database import get_db
from app.services.incident_service import IncidentService
from app.schemas.incident import (
    IncidentReportRequest, 
    IncidentStatusUpdate, 
    IncidentResponse, 
    IncidentListResponse,
    ApiResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/fire", tags=["Fire Department"])


@router.post("/report-incident", 
             response_model=ApiResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Report a fire incident",
             description="Allows residents, fire department, and law enforcement to report fire incidents")
async def report_fire_incident(
    incident_data: IncidentReportRequest,
    db: Session = Depends(get_db)
) -> ApiResponse:
    """
    Report a new fire incident
    
    - **user_id**: ID of the user reporting the incident
    - **location**: General location of the fire incident
    - **address**: Specific address of the fire incident
    - **description**: Detailed description of the fire incident
    """
    try:
        service = IncidentService(db)
        incident = service.create_incident(incident_data)
        
        logger.info(f"Fire incident {incident.id} reported successfully")
        
        return ApiResponse(
            success=True,
            message="Fire incident reported successfully",
            data={
                "incident_id": incident.id,
                "status": incident.status,
                "created_at": incident.created_at.isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to report fire incident: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to report fire incident"
        )


@router.post("/status",
             response_model=IncidentResponse,
             summary="Update fire incident status",
             description="Update the status of a fire incident report")
async def update_fire_incident_status(
    incident_id: int,
    status_data: IncidentStatusUpdate,
    db: Session = Depends(get_db)
) -> IncidentResponse:
    """
    Update the status of a fire incident
    
    - **incident_id**: ID of the incident to update
    - **status**: New status for the incident (REPORTED, IN_PROGRESS, RESOLVED, CLOSED)
    """
    try:
        service = IncidentService(db)
        incident = service.update_incident_status(incident_id, status_data)
        
        if not incident:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Fire incident with ID {incident_id} not found"
            )
        
        logger.info(f"Fire incident {incident_id} status updated to {status_data.status}")
        return incident
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update fire incident status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update fire incident status"
        )


@router.get("/incident/{incident_id}",
            response_model=IncidentResponse,
            summary="Get fire incident details",
            description="Retrieve details of a specific fire incident")
async def get_fire_incident(
    incident_id: int,
    db: Session = Depends(get_db)
) -> IncidentResponse:
    """
    Get fire incident details by ID
    
    - **incident_id**: ID of the incident to retrieve
    """
    try:
        service = IncidentService(db)
        incident = service.get_incident_by_id(incident_id)
        
        if not incident:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Fire incident with ID {incident_id} not found"
            )
        
        return incident
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve fire incident: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve fire incident"
        )


@router.get("/incidents",
            response_model=IncidentListResponse,
            summary="List fire incidents",
            description="Get paginated list of fire incidents with optional filtering")
async def list_fire_incidents(
    page: int = 1,
    size: int = 10,
    status_filter: Optional[str] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
) -> IncidentListResponse:
    """
    Get paginated list of fire incidents
    
    - **page**: Page number (default: 1)
    - **size**: Items per page (default: 10)
    - **status_filter**: Filter by incident status
    - **user_id**: Filter by user ID
    """
    try:
        service = IncidentService(db)
        incidents, total = service.get_incidents(page, size, status_filter, user_id)
        
        total_pages = (total + size - 1) // size
        
        return IncidentListResponse(
            incidents=incidents,
            total=total,
            page=page,
            size=size,
            total_pages=total_pages
        )
        
    except Exception as e:
        logger.error(f"Failed to list fire incidents: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list fire incidents"
        ) 