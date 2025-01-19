async def test_add_booking(db, authenticated_client):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_client.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": "2025-01-12",
            "date_to": "2025-01-13",
        }
    )
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, dict)
    assert result["status"] == "OK"
    assert "data" in result