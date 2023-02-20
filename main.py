from typing import List, Dict, Optional

from fastapi import FastAPI
from pydantic import BaseModel
from random import randrange

hotels = [
    {
        "id": 1,
        "title": "Mercure hotel",
        "content": "8 nghts, 3 persons",
        "booked": False,
        "rating": True,
    },
    {
        "id": 2,
        "title": "Blue Radisson",
        "content": "7 nghts, 3 persons",
        "booked": False,
        "rating": True,
    },
    {
        "id": 3,
        "title": "Plaza",
        "content": "5 nghts, 3 persons",
        "booked": False,
        "rating": True,
    },
]


class Hotel(BaseModel):
    title: str
    content: str | None = None
    booked: bool | None = True
    rating: Optional[bool | str] = None


app = FastAPI()


@app.get('/hotels')
def get_hotels():
    return {"data": hotels}


@app.get('/hotels/{id}')
def get_hotel_data():
    pass


@app.post("/hotels")
def book_hotel(hotel: Hotel) -> Dict[str, dict]:
    booked_hotel = hotel.dict()
    booked_hotel["id"] = randrange(0, 1000000)
    hotels.append(booked_hotel)

    return {"data": booked_hotel}
