import shutil
from fastapi import UploadFile
from app.services.base import BaseService
from app.tasks.tasks import save_images_in_different_qualities


class ImageService(BaseService):
    def upload_image(file: UploadFile):
        image_path = f"app/static/images/{file.filename}"
        with open(image_path, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)

        save_images_in_different_qualities.delay(image_path)
