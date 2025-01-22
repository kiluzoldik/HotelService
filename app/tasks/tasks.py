import os
import asyncio
from time import sleep

from PIL import Image

from app.tasks.celery_app import celery_instance
from app.utils.db_manager import DBManager
from app.database import async_session_maker_null_pool


@celery_instance.task
def test_task():
    sleep(5)
    print("completed task")


@celery_instance.task
def save_images_in_different_qualities(image_path: str):
    # Открываем изображение
    try:
        with Image.open(image_path) as img:
            IMAGES_FORMATS = [1000, 500, 200]
            # Проверяем формат изображения
            img_format = img.format

            # Уменьшаем изображение и сохраняем его в разных размерах
            for size in IMAGES_FORMATS:
                # Пропорциональное изменение размера
                aspect_ratio = img.height / img.width
                new_height = int(size * aspect_ratio)
                resized_img = img.resize((size, new_height), Image.LANCZOS)

                # Генерируем имя файла
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                save_path = os.path.join(
                    "app/static/images", f"{base_name}_{size}px.{img_format.lower()}"
                )

                # Сохраняем файл
                resized_img.save(save_path, format=img_format)

    except Exception as e:
        print(f"Ошибка при обработке изображения: {e}")


async def get_bookings_with_today_checkin_helper():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings=}")


@celery_instance.task(name="booking_today_checkin")
def send_emails_to_users_with_booking_today():
    asyncio.run(get_bookings_with_today_checkin_helper())
