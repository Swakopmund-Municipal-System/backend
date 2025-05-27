"""
Business logic for incident management
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import date
import logging

from app.models.incident import PublicSafetyIncidentReport
from app.schemas.incident import IncidentReportRequest, IncidentStatusUpdate, IncidentStatus
from app.core.database import get_db

logger = logging.getLogger(__name__)


class IncidentService:
    """Service class for incident management operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_incident(self, incident_data: IncidentReportRequest) -> PublicSafetyIncidentReport:
        """
        Create a new incident report
        
        Args:
            incident_data: Validated incident data from request
            
        Returns:
            Created incident record
            
        Raises:
            Exception: If incident creation fails
        """
        try:
            db_incident = PublicSafetyIncidentReport(
                description=incident_data.description,
                location=incident_data.location,
                address=incident_data.address,
                user_id=incident_data.user_id,
                date=date.today(),
                status=IncidentStatus.REPORTED.value
            )
            
            self.db.add(db_incident)
            self.db.commit()
            self.db.refresh(db_incident)
            
            logger.info(f"Created incident {db_incident.id} for user {incident_data.user_id}")
            return db_incident
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create incident: {str(e)}")
            raise
    
    def get_incident_by_id(self, incident_id: int) -> Optional[PublicSafetyIncidentReport]:
        """
        Retrieve incident by ID
        
        Args:
            incident_id: The incident ID to retrieve
            
        Returns:
            Incident record if found, None otherwise
        """
        return self.db.query(PublicSafetyIncidentReport).filter(
            PublicSafetyIncidentReport.id == incident_id
        ).first()
    
    def update_incident_status(self, incident_id: int, status_data: IncidentStatusUpdate) -> Optional[PublicSafetyIncidentReport]:
        """
        Update incident status
        
        Args:
            incident_id: The incident ID to update
            status_data: New status data
            
        Returns:
            Updated incident record if found, None otherwise
            
        Raises:
            Exception: If update fails
        """
        try:
            incident = self.get_incident_by_id(incident_id)
            if not incident:
                return None
            
            incident.status = status_data.status.value
            self.db.commit()
            self.db.refresh(incident)
            
            logger.info(f"Updated incident {incident_id} status to {status_data.status.value}")
            return incident
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to update incident {incident_id}: {str(e)}")
            raise
    
    def get_incidents(self, 
                      page: int = 1, 
                      size: int = 10, 
                      status: Optional[str] = None,
                      user_id: Optional[int] = None) -> tuple[List[PublicSafetyIncidentReport], int]:
        """
        Retrieve paginated list of incidents with optional filtering
        
        Args:
            page: Page number (1-based)
            size: Number of items per page
            status: Optional status filter
            user_id: Optional user ID filter
            
        Returns:
            Tuple of (incidents_list, total_count)
        """
        query = self.db.query(PublicSafetyIncidentReport)
        
        # Apply filters
        if status:
            query = query.filter(PublicSafetyIncidentReport.status == status)
        if user_id:
            query = query.filter(PublicSafetyIncidentReport.user_id == user_id)
        
        # Get total count
        total = query.count()
        
        # Apply pagination and ordering
        incidents = query.order_by(desc(PublicSafetyIncidentReport.created_at))\
                        .offset((page - 1) * size)\
                        .limit(size)\
                        .all()
        
        return incidents, total


def get_incident_service(db: Session = next(get_db())) -> IncidentService:
    """
    Dependency injection for incident service
    """
    return IncidentService(db) 