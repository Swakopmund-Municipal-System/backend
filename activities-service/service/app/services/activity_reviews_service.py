from typing import List, Optional
import uuid

from sqlalchemy import text
from sqlalchemy.orm import Session
from app.models.db.models import Activity, ActivityImage, ActivityReview, Image
from app.models.dto.models import (
    ActivityReviewSearchResultDTO,
    CreateReviewDTO,
)


def search_activity_reviews(
    db: Session,
    search_term: str,
    sort_field: str,
    sort_order: str = "asc",
    limit: int = 10,
    page: int = 1,
    activity_id: int = 0,
) -> list[ActivityReviewSearchResultDTO]:
    try:
        if sort_order not in ["asc", "desc"]:
            sort_order = "asc"

        if sort_field not in ["id", "rating", "created_at"]:
            sort_field = ""

        if page < 1:
            page = 1

        offset = (page - 1) * limit

        query = (
            db.query(ActivityReview)
            .filter((ActivityReview.review_text.ilike(f"%{search_term}%")))
            .filter((ActivityReview.activity_id == activity_id))
        )

        if len(sort_field) > 0:
            if sort_order == "asc":
                query = query.order_by(getattr(ActivityReview, sort_field).asc())
            else:
                query = query.order_by(getattr(ActivityReview, sort_field).desc())

        data = query.offset(offset).limit(limit).all()

        return_data = [
            ActivityReviewSearchResultDTO(
                id=item.id,
                activity_id=item.activity_id,
                user_id=str(item.user_id),
                review_text=item.review_text,
                rating=item.rating,
                created_at=item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            )
            for item in data
        ]

        return return_data
    except Exception as e:
        print(f"Error searching activity reviews: {e}")
        return []


def create_activity_review(
    db: Session, data: CreateReviewDTO, user_id: int
) -> tuple[int, int, str]:
    try:

        activity = db.query(Activity).filter(Activity.id == data.activity_id).first()
        if not activity:
            return None, 404, "Activity not found"

        insert_data = ActivityReview(
            activity_id=data.activity_id,
            user_id=user_id,
            review_text=data.review,
            rating=data.rating,
            created_at=text("NOW()"),
        )
        db.add(insert_data)
        db.flush()

        db.commit()

        return insert_data.id, 201, "Review created successfully"
    except Exception as e:
        db.rollback()
        print(f"Error creating review: {e}")
        return None, 500, str(e)


def delete_activity_review_by_id(db: Session, review_id: int) -> tuple[bool, int, str]:
    try:
        delete_data = (
            db.query(ActivityReview).filter(ActivityReview.id == review_id).first()
        )
        if not delete_data:
            return False, 404, "Review not found"

        db.delete(delete_data)
        db.commit()

        return True, 200, "Review deleted successfully"
    except Exception as e:
        db.rollback()
        print(f"Error deleting review: {e}")
        return False, 500, str(e)
