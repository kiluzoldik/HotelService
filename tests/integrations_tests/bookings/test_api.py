import pytest

from app.utils.db_manager import DBManager
from app.database import async_session_maker_null_pool


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2025-01-12", "2025-01-18", 200),
        (1, "2025-01-13", "2025-01-19", 200),
        (1, "2025-01-14", "2025-01-20", 200),
        (1, "2025-01-15", "2025-01-21", 200),
        (1, "2025-01-16", "2025-01-22", 200),
        (1, "2025-01-17", "2025-01-23", 409),
        (1, "2025-02-12", "2025-02-13", 200),
    ],
)
async def test_add_booking(room_id, date_from, date_to, status_code, authenticated_client):
    response = await authenticated_client.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == status_code
    if status_code == 200:
        result = response.json()
        assert isinstance(result, dict)
        assert result["status"] == "OK"
        assert "data" in result


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.bookings.delete()
        await db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, count",
    [
        (1, "2025-01-12", "2025-01-18", 1),
        (1, "2025-01-13", "2025-01-19", 2),
        (1, "2025-01-14", "2025-01-20", 3),
    ],
)
async def test_add_and_get_bookings(
    room_id, date_from, date_to, count, delete_all_bookings, authenticated_client
):
    response_bookings = await authenticated_client.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response_bookings.status_code == 200
    response_bookings_me = await authenticated_client.get("/bookings/me")
    result = response_bookings_me.json()
    assert len(result) == count
