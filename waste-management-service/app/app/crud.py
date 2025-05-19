import datetime
import uuid
from sqlalchemy.orm import Session

from app.models.db.models import MissedWastePickups
from app.models.dto.models import (
    CreateMissedWastePickupDto,
    MissedWastePickupSearchResultDto,
    UpdateMissedWastePickupStatusDto,
)
from app.models.enums.enums import MissedWastePickupStatusEnum

# ---- missed_waste_pickups ----


def create_missed_waste_pickup(
    db: Session, data: CreateMissedWastePickupDto, userId: int
) -> tuple[MissedWastePickups, int, str]:
    try:
        if not data.description or not data.date or not data.address:
            return None, 400, "Invalid input data"

        if (
            not data.description.strip()
            or not data.date.strip()
            or not data.address.strip()
        ):
            return None, 400, "Invalid input data"

        if len(data.description) > 255:
            return None, 400, "Description is too long"

        if len(data.address) > 255:
            return None, 400, "Address is too long"

        date_as_datetime = datetime.datetime.strptime(data.date, "%Y-%m-%d %H:%M:%S")

        missed_waste_pickup = MissedWastePickups(
            description=data.description,
            date=date_as_datetime,
            address=data.address,
            status=MissedWastePickupStatusEnum.PENDING_REVIEW,
            userId=userId,
        )

        db.add(missed_waste_pickup)
        db.commit()
        db.refresh(missed_waste_pickup)
        return missed_waste_pickup, 201, ""
    except Exception as e:
        print(f"Error creating missed waste pickup: {e}")
        return None, 500, "An error occurred while creating the missed waste pickup"


def search_missed_waste_pickups(
    db: Session,
    search_term: str,
    sort_field: str,
    sort_order: str = "asc",
    limit: int = 10,
    page: int = 1,
) -> list[MissedWastePickupSearchResultDto]:
    try:
        if sort_order not in ["asc", "desc"]:
            sort_order = "asc"

        if sort_field not in ["date", "status", "userId", "id"]:
            sort_field = ""

        if page < 1:
            page = 1

        offset = (page - 1) * limit

        query = db.query(MissedWastePickups).filter(
            (MissedWastePickups.description.ilike(f"%{search_term}%"))
            | (MissedWastePickups.address.ilike(f"%{search_term}%"))
        )

        if len(sort_field) > 0:
            if sort_order == "asc":
                query = query.order_by(getattr(MissedWastePickups, sort_field).asc())
            else:
                query = query.order_by(getattr(MissedWastePickups, sort_field).desc())

        missed_waste_pickups = query.offset(offset).limit(limit).all()

        return_data = [
            MissedWastePickupSearchResultDto(
                id=item.id,
                description=item.description,
                date=item.date.strftime("%Y-%m-%d %H:%M:%S"),
                address=item.address,
                status=item.status,
                userId=str(item.userId),
            )
            for item in missed_waste_pickups
        ]

        return return_data
    except Exception as e:
        print(f"Error searching missed waste pickups: {e}")
        return []


def get_missed_waste_pickup_details(
    db: Session, id: int
) -> MissedWastePickupSearchResultDto | None:
    try:
        item: MissedWastePickups = db.query(MissedWastePickups).get(id)
        if not item:
            return None

        return MissedWastePickupSearchResultDto(
            id=item.id,
            description=item.description,
            date=item.date.strftime("%Y-%m-%d %H:%M:%S"),
            address=item.address,
            status=item.status,
            userId=str(item.userId),
        )

    except Exception as e:
        print(f"Error getting missed waste pickups: {e}")
        return None


def update_missed_waste_pickup_status(
    db: Session, data: UpdateMissedWastePickupStatusDto
) -> tuple[bool, int, str]:
    try:
        missed_waste_pickup = (
            db.query(MissedWastePickups)
            .filter(MissedWastePickups.id == data.id)
            .first()
        )

        if not missed_waste_pickup:
            return False, 404, "Missed waste pickup not found"

        if data.status not in [
            MissedWastePickupStatusEnum.PENDING_REVIEW,
            MissedWastePickupStatusEnum.REVIEWED,
        ]:
            return False, 400, "Invalid status value"

        missed_waste_pickup.status = data.status
        db.commit()
        return True, 200, ""
    except Exception as e:
        print(f"Error updating missed waste pickup status: {e}")
        return (
            False,
            500,
            "An error occurred while updating the missed waste pickup status",
        )


# ---- end of missed_waste_pickups ----
