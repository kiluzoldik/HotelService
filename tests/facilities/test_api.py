from httpx import AsyncClient


async def test_add_facility(ac: AsyncClient):
    response = await ac.post(
        "/facilities",
        json={
            "title": "Сауна",
        }
    )
    print(f"{response.json()=}")
    
    assert response.status_code == 200

async def test_get_facilities(ac: AsyncClient):
    response = await ac.get(
        "/facilities",
    )
    print(f"{response.json()=}")
    
    assert response.status_code == 200