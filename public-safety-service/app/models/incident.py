"""
Incident model for Public Safety Service
"""
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import date, datetime

from app.core.database import Base


class PublicSafetyIncidentReport(Base):
    """
    Model for Public Safety Incident Reports
    
    Represents fire, law enforcement, and emergency response incidents
    """
    __tablename__ = "public_safety_incident_reports"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(Text, nullable=False)
    date = Column(Date, nullable=False, default=date.today)
    location = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="REPORTED")
    user_id = Column(Integer, nullable=False)  # FK reference (simplified for this example)
    
    # Audit fields
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<PublicSafetyIncidentReport(id={self.id}, status={self.status}, location={self.location})>" 