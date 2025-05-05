import datetime
from typing import List, Optional
import uuid

from sqlalchemy import text
from sqlalchemy.orm import Session
from app.models.db.models import Activity, ActivityImage, ActivityReview, Image
from app.models.dto.models import (
    ActivityCreateDTO,
    ActivityDetailDTO,
    ActivityEditDTO,
    ActivitySearchResultDTO,
)


def search_activities(
    db: Session,
    search_term: str,
    sort_field: str,
    sort_order: str = "asc",
    limit: int = 10,
    page: int = 1,
    categories: Optional[str] = None,
) -> list[ActivitySearchResultDTO]:
    try:
        if sort_order not in ["asc", "desc"]:
            sort_order = "asc"

        if sort_field not in ["id", "name", "created_at", "updated_at"]:
            sort_field = ""

        if page < 1:
            page = 1

        offset = (page - 1) * limit

        query = db.query(Activity).filter(
            (Activity.name.ilike(f"%{search_term}%"))
            | (Activity.description.ilike(f"%{search_term}%"))
        )

        if categories and len(categories) > 0:
            category_list = categories.split(",")
            query = query.filter(Activity.type.in_(category_list))

        if len(sort_field) > 0:
            if sort_order == "asc":
                query = query.order_by(getattr(Activity, sort_field).asc())
            else:
                query = query.order_by(getattr(Activity, sort_field).desc())

        data = query.offset(offset).limit(limit).all()

        return_data = [
            ActivitySearchResultDTO(
                id=item.id,
                name=item.name,
                description=item.description,
                booking_url=item.booking_url,
                type=item.type,
                image_id=item.hero_image_id,
                latitude=item.latitude,
                longitude=item.longitude,
                createdAt=item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                updatedAt=item.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                address=item.address,
            )
            for item in data
        ]

        return return_data
    except Exception as e:
        print(f"Error searching activities: {e}")
        return []


def search_activities_by_location(
    db: Session,
    latitude: float,
    longitude: float,
    radius: int = 1000,
    search_term: str = "",
    categories: Optional[str] = None,
) -> list[ActivitySearchResultDTO]:
    try:
        query = db.query(Activity).filter(
            (Activity.name.ilike(f"%{search_term}%"))
            | (Activity.description.ilike(f"%{search_term}%"))
        )

        if categories and len(categories) > 0:
            category_list = categories.split(",")
            query = query.filter(Activity.type.in_(category_list))

        query = query.filter(
            text(
                f"ST_DWithin(point_geom, ST_MakePoint({longitude}, {latitude})::geography, {radius})"
            )
        )

        data = query.all()

        return_data = [
            ActivitySearchResultDTO(
                id=item.id,
                name=item.name,
                description=item.description,
                booking_url=item.booking_url,
                type=item.type,
                image_id=item.hero_image_id,
                latitude=item.latitude,
                longitude=item.longitude,
                createdAt=item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                updatedAt=item.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                address=item.address,
            )
            for item in data
        ]

        return return_data
    except Exception as e:
        print(f"Error searching activities by location: {e}")
        return []


def get_activity_by_id(
    db: Session, activity_id: int
) -> tuple[ActivityDetailDTO, int, str]:
    try:
        activity_data = db.query(Activity).filter(Activity.id == activity_id).first()
        if not activity_data:
            return None, 404, "Activity not found"

        return_data = ActivityDetailDTO(
            id=activity_data.id,
            name=activity_data.name,
            description=activity_data.description,
            address=activity_data.address,
            type=activity_data.type,
            createdAt=activity_data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            updatedAt=activity_data.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            latitude=activity_data.latitude,
            longitude=activity_data.longitude,
            booking_url=activity_data.booking_url,
            hero_image_id=activity_data.hero_image_id,
        )

        return return_data, 200, "Activity retrieved successfully"
    except Exception as e:
        print(f"Error retrieving activity: {e}")
        return None, 500, str(e)


def create_activity(
    db: Session, data: ActivityCreateDTO, user_id: int
) -> tuple[int, int, str]:
    try:
        hero_image_data = None
        if data.hero_image != None:
            hero_image_data = Image(
                name=data.hero_image.filename,
                filepath=uuid.uuid4().hex.replace("-", "") + data.hero_image.filename,
            )
            db.add(hero_image_data)
            db.flush()

            fileSavePath = f"uploads/{hero_image_data.filepath}"
            with open(fileSavePath, "wb") as f:
                f.write(data.hero_image.file.read())

        activity_data = Activity(
            name=data.name,
            type=data.type,
            description=data.description,
            address=data.address,
            created_by=user_id,
            updated_by=user_id,
            booking_url=data.booking_url,
            hero_image_id=hero_image_data.id if hero_image_data else None,
            latitude=data.latitude,
            longitude=data.longitude,
            created_at=datetime.datetime.now(datetime.timezone.utc),
            updated_at=datetime.datetime.now(datetime.timezone.utc),
            point_geom=f"SRID=4326;POINT({data.longitude} {data.latitude})",
        )
        db.add(activity_data)
        db.flush()

        for image in data.files:
            image_data = Image(
                name=image.filename,
                filepath=uuid.uuid4().hex.replace("-", "") + image.filename,
            )
            db.add(image_data)
            db.flush()

            activity_image_data = ActivityImage(
                image_id=image_data.id,
                activity_id=activity_data.id,
            )
            db.add(activity_image_data)
            db.flush()

            fileSavePath = f"uploads/{image_data.filepath}"
            with open(fileSavePath, "wb") as f:
                f.write(image.file.read())

        db.commit()

        return activity_data.id, 201, "Activity created successfully"
    except Exception as e:
        db.rollback()
        print(f"Error creating activity: {e}")
        return None, 500, str(e)


def edit_activity(
    db: Session, data: ActivityEditDTO, user_id: int
) -> tuple[bool, int, str]:
    try:
        activity_data = db.query(Activity).filter(Activity.id == data.id).first()
        if not activity_data:
            return False, 404, "Activity not found"

        activity_data.name = data.name
        activity_data.description = data.description
        activity_data.address = data.address
        activity_data.booking_url = data.booking_url
        activity_data.latitude = data.latitude
        activity_data.longitude = data.longitude
        activity_data.updated_by = user_id
        activity_data.updated_at = datetime.datetime.now(datetime.timezone.utc)

        db.commit()

        return True, 200, "Activity updated successfully"
    except Exception as e:
        db.rollback()
        print(f"Error updating activity: {e}")
        return False, 500, str(e)


def delete_activity_by_id(db: Session, activity_id: int) -> tuple[bool, int, str]:
    try:
        activity_data = db.query(Activity).filter(Activity.id == activity_id).first()
        if not activity_data:
            return False, 404, "Activity not found"

        db.query(ActivityImage).filter(
            ActivityImage.activity_id == activity_id
        ).delete()
        db.query(ActivityReview).filter(
            ActivityReview.activity_id == activity_id
        ).delete()

        db.delete(activity_data)
        db.commit()

        return True, 200, "Activity deleted successfully"
    except Exception as e:
        db.rollback()
        print(f"Error deleting activity: {e}")
        return False, 500, str(e)
