from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()

class PermitStatusEnum(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    IN_REVIEW = "in_review"

class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(255), nullable=False)
    owner_name = Column(String(100), nullable=False)
    property_type = Column(String(50), nullable=False)
    size = Column(Float, nullable=False)
    zoning = Column(String(50), nullable=False)
    last_valuation_date = Column(DateTime)
    valuations = relationship("PropertyValuation", back_populates="property")
    permits = relationship("PermitApplication", back_populates="property")

class PropertyValuation(Base):
    __tablename__ = "property_valuations"
    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    value = Column(Float, nullable=False)
    valuation_date = Column(DateTime)
    assessed_by = Column(String(100))
    notes = Column(Text)
    property = relationship("Property", back_populates="valuations")

class PermitApplication(Base):
    __tablename__ = "permit_applications"
    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    applicant_name = Column(String(100))
    application_type = Column(String(100))
    description = Column(Text)
    status = Column(Enum(PermitStatusEnum), default=PermitStatusEnum.PENDING)
    submission_date = Column(DateTime)
    development_plans = Column(Text)  # Could be a JSON or text field
    property = relationship("Property", back_populates="permits")
