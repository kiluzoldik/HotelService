from app.utils.db_manager import DBManager


async def test_add_booking(db: DBManager, authenticated_client):
    room_id = (await db.rooms.get_all())[0].id
    date_from = "2025-01-12"
    date_to = "2025-01-13"
    response_1 = await authenticated_client.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    response_2 = await authenticated_client.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response_1.status_code == 200
    assert response_2.status_code == 409
    result = response_1.json()
    assert isinstance(result, dict)
    assert result["status"] == "OK"
    assert "data" in result
