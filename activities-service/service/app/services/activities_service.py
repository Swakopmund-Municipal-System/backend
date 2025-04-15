import uuid
from pytest import Session

from app.models.db.models import Activity, ActivityImage, Image
from app.models.dto.models import ActivityCreateDTO, ActivitySearchResultDTO


def search_activities(
    db: Session,
    search_term: str,
    sort_field: str,
    sort_order: str = "asc",
    limit: int = 10,
    page: int = 1,
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


def create_activity(db: Session, data: ActivityCreateDTO) -> tuple[int, int, str]:
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
            description=data.description,
            address=data.address,
            created_by=uuid.uuid4(),
            updated_by=uuid.uuid4(),
            booking_url=data.booking_url,
            hero_image_id=hero_image_data.id if hero_image_data else None,
            latitude=data.latitude,
            longitude=data.longitude,
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

        db.commit()

        return activity_data.id, 201, "Activity created successfully"
    except Exception as e:
        db.rollback()
        print(f"Error creating activity: {e}")
        return None, 500, str(e)
