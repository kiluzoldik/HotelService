from fastapi import APIRouter, UploadFile

from app.services.images import ImageService


router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("")
def upload_image(file: UploadFile):
    ImageService().upload_image(file)
