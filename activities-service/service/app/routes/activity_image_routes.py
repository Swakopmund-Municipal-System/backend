import os
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.db.models import Image
from app.services.activity_images_service import (
    add_images_for_activity,
    get_image_ids_for_activity,
    set_hero_image_for_activity,
)

router = APIRouter()


@router.get(
    "/{image_id}",
    responses={
        200: {"description": "Image retrieved successfully."},
        404: {"description": "Image not found."},
        500: {"description": "Internal server error."},
    },
)
def get_image(
    image_id: int,
    db: Session = Depends(get_db),
):
    try:
        image_data = db.query(Image).filter(Image.id == image_id).first()
        if not image_data:
            raise HTTPException(status_code=404, detail="Image not found")

        file_path = f"uploads/{image_data.filepath}"
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(file_path)

    except Exception as e:
        print(f"Error retrieving image: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/activity/{activity_id}/hero/upload",
    responses={
        201: {"description": "Image uploaded successfully."},
        400: {"description": "Invalid input data."},
        500: {"description": "Internal server error."},
    },
)
def upload_hero_image(
    activity_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        (success, status_code, err_message) = set_hero_image_for_activity(
            db, activity_id, image
        )
        if not success:
            raise HTTPException(status_code=status_code, detail=err_message)

        return JSONResponse(
            status_code=status_code,
            content={"message": "Image uploaded successfully."},
        )

    except Exception as e:
        print(f"Error uploading image: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/activity/{activity_id}/upload",
    responses={
        201: {"description": "Images uploaded successfully."},
        400: {"description": "Invalid input data."},
        500: {"description": "Internal server error."},
    },
)
def upload_activity_images(
    activity_id: int,
    images: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    try:
        (success, status_code, err_message) = add_images_for_activity(
            db, activity_id, images
        )
        if not success:
            raise HTTPException(status_code=status_code, detail=err_message)

        return JSONResponse(
            status_code=201,
            content={"message": "Images uploaded successfully."},
        )

    except Exception as e:
        print(f"Error uploading images: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/activity/{activity_id}",
    responses={
        200: {"description": "images retrieved successfully."},
        404: {"description": "activity not found."},
        500: {"description": "Internal server error."},
    },
)
def get_activity_images(
    activity_id: int,
    db: Session = Depends(get_db),
):
    try:
        (image_ids, status_code, err_message) = get_image_ids_for_activity(
            db, activity_id
        )
        if not image_ids:
            raise HTTPException(status_code=status_code, detail=err_message)

        return JSONResponse(
            status_code=200,
            content={"image_ids": image_ids},
        )

    except Exception as e:
        print(f"Error retrieving images: {e}")
        raise HTTPException(status_code=500, detail=str(e))
