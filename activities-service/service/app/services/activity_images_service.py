import os
import uuid
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.db.models import Activity, ActivityImage, Image


def set_hero_image_for_activity(
    db: Session, activity_id: int, file: UploadFile
) -> tuple[bool, int, str]:
    try:

        activity = db.query(Activity).filter(Activity.id == activity_id).first()
        if not activity:
            return None, 404, "Activity not found"

        image_data = Image(
            name=file.filename,
            filepath=uuid.uuid4().hex.replace("-", "") + file.filename,
        )
        db.add(image_data)
        db.flush()

        fileSavePath = f"uploads/{image_data.filepath}"
        with open(fileSavePath, "wb") as f:
            f.write(file.file.read())

        activity.hero_image_id = image_data.id
        db.commit()

        return True, 201, "upload successful"
    except Exception as e:
        db.rollback()
        print(f"Failed to upload hero image: {e}")
        return None, 500, str(e)


def add_images_for_activity(
    db: Session, activity_id: int, files: list[UploadFile]
) -> tuple[bool, int, str]:
    try:
        activity = db.query(Activity).filter(Activity.id == activity_id).first()
        if not activity:
            return None, 404, "Activity not found"

        for file in files:
            image_data = Image(
                name=file.filename,
                filepath=uuid.uuid4().hex.replace("-", "") + file.filename,
            )
            db.add(image_data)
            db.flush()

            activity_image_data = ActivityImage(
                image_id=image_data.id,
                activity_id=activity_id,
            )
            db.add(activity_image_data)
            db.flush()

            fileSavePath = f"uploads/{image_data.filepath}"
            with open(fileSavePath, "wb") as f:
                f.write(file.file.read())

        db.commit()

        return True, 201, "upload successful"
    except Exception as e:
        db.rollback()
        print(f"Failed to upload images: {e}")
        return None, 500, str(e)


def get_image_ids_for_activity(
    db: Session, activity_id: int
) -> tuple[list[int], int, str]:
    try:
        activity = db.query(Activity).filter(Activity.id == activity_id).first()
        if not activity:
            return None, 404, "Activity not found"

        activity_images = (
            db.query(ActivityImage)
            .filter(ActivityImage.activity_id == activity_id)
            .all()
        )

        return (
            [image.image_id for image in activity_images],
            200,
            "Images retrieved successfully",
        )
    except Exception as e:
        print(f"Failed to retrieve images: {e}")
        return None, 500, str(e)


def delete_image_by_id(db: Session, image_id: int) -> tuple[bool, int, str]:
    try:
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            return None, 404, "Image not found"

        db.delete(image)
        db.commit()

        if os.path.exists(f"uploads/{image.filepath}"):
            os.remove(f"uploads/{image.filepath}")

        return True, 200, "Image deleted successfully"
    except Exception as e:
        db.rollback()
        print(f"Failed to delete image: {e}")
        return None, 500, str(e)
