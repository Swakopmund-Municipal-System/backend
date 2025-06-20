from geoalchemy2 import Geometry
from sqlalchemy import (
    TIMESTAMP,
    BigInteger,
    Column,
    Float,
    ForeignKey,
    Integer,
    PrimaryKeyConstraint,
    String,
    UUID,
)
from sqlalchemy.orm import relationship
from ...database import Base


class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(Integer, index=False)
    name = Column(String(255), index=False)
    description = Column(String(512), index=False)
    address = Column(String(255), index=False)
    created_at = Column(TIMESTAMP, index=False)
    updated_at = Column(TIMESTAMP, index=False)
    created_by = Column(BigInteger, index=True)
    updated_by = Column(BigInteger, index=True)

    booking_url = Column(String(255), index=False)
    hero_image_id = Column(
        Integer, ForeignKey("images.id", ondelete="SET NULL"), nullable=True, index=True
    )

    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)
    point_geom = Column(Geometry(geometry_type="POINT", srid=4326))

    reviews = relationship("ActivityReview", back_populates="activity")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    filepath = Column(String(512), nullable=False)


class ActivityImage(Base):
    __tablename__ = "activity_images"
    __table_args__ = (PrimaryKeyConstraint("image_id", "activity_id"),)

    image_id = Column(
        Integer, ForeignKey("images.id", ondelete="CASCADE"), nullable=False
    )

    activity_id = Column(
        Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False
    )


class ActivityReview(Base):
    __tablename__ = "activity_reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    activity_id = Column(
        Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(BigInteger, index=True)
    rating = Column(Integer, index=False)
    review_text = Column(String(512), index=False)
    activity = relationship("Activity", back_populates="reviews")

    created_at = Column(TIMESTAMP, index=False)
