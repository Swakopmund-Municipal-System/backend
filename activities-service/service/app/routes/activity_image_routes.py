from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def list_activities():
    return {"message": "List of images"}
