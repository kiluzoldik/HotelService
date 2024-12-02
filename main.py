from typing import Annotated
from fastapi import FastAPI, Form
import uvicorn


app = FastAPI()

hotels = [
    {"id": 1, "title": "Hotel A", "name": "sochi"},
    {"id": 2, "title": "Hotel B", "name": "moscow"},
]


@app.get("/hotels")
async def get_hotels():
    return hotels


@app.get("/hotels/{hotel_id}")
async def get_hotel(hotel_id: int):
    return [hotel for hotel in hotels if hotel["id"] == hotel_id]


@app.post("/hotels")
async def create_hotel(
    title: Annotated[str, Form()],
    name: Annotated[str, Form()],
):
    hotels.append({"id": hotels[-1]["id"] + 1, "title": title, "name": name})
    return {"message": "Отель успешно добавлен"}


@app.delete("/hotels/{hotel_id}")
async def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"message": "Отель успешно удален"}


@app.put("/hotels/{hotel_id}")
async def full_update_hotel(
    hotel_id: int,
    title: Annotated[str, Form()],
    name: Annotated[str, Form()],
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return {"message": "Отель успешно изменен"}
    return {"message": "Отель не найден"}


@app.patch("/hotels/{hotel_id}")
async def partial_update_hotel(
    hotel_id: int,
    title: Annotated[str, Form()] = None,
    name: Annotated[str, Form()] = None,
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title:
                hotel["title"] = title
            if name:
                hotel["name"] = name
            return {"message": "Отель успешно изменен"}
    return {"message": "Отель не найден"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)