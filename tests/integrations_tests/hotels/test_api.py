from httpx import AsyncClient


async def test_get_hotels(ac: AsyncClient):
    response = await ac.get(
        "/hotels",
        params={
            "date_from": "2025-01-12",
            "date_to": "2025-01-13",
        }
    )
    print(f"{response.json()=}")
    
    assert response.status_code == 200