from typing import List, Dict, Optional

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from random import randrange

hotels = [
    {
        "id": 1,
        "title": "Mercure hotel",
        "content": "8 nghts, 3 persons",
        "booked": False,
        "rating": True,
        "data": "Test"
    },
    {
        "id": 2,
        "title": "Blue Radisson",
        "content": "7 nghts, 3 persons",
        "booked": False,
        "rating": True,
        "data": "Test"
    },
    {
        "id": 3,
        "title": "Plaza",
        "content": "5 nghts, 3 persons",
        "booked": False,
        "rating": True,
        "data": "Test"
    },
]


class Hotel(BaseModel):
    title: str
    content: str | None = None
    booked: bool | None = True
    rating: Optional[bool | str] = None

    def add_hotel(self, data: str) -> Dict[str, dict]:
        added_hotel = self.dict()
        added_hotel["id"] = randrange(0, 1000000)
        added_hotel["data"] = data
        hotels.append(added_hotel)

        return added_hotel

    @staticmethod
    def find_hotel_idx(id: int) -> int | None:
        for i, hotel in enumerate(hotels):
            if hotel['id'] == id:
                return i

        return None

    @staticmethod
    def delete_hotel(id: int) -> Dict[str, str | int | bool] | None:
        deleted_hotel_idx = Hotel.find_hotel_idx(id)

        if deleted_hotel_idx != None:
            deleted_hotel = hotels.pop(deleted_hotel_idx)

            return deleted_hotel

        return None


app = FastAPI()


@app.get('/hotels')
def get_all_hotels() -> Dict[str, List[Dict[str, str | int | bool]]]:
    return {"data": hotels}


@app.get('/hotels/{id}')
def get_hotel_details(id: int) -> Dict[str, str | int | bool] | None:
    found_hotel_idx = Hotel.find_hotel_idx(id)

    if found_hotel_idx == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Hotel with id {id} not found")

    return hotels[found_hotel_idx]


@app.post("/hotels", status_code=status.HTTP_201_CREATED)
def add_hotel(hotel: Hotel) -> Dict[str, dict]:
    added_hotel = hotel.add_hotel('Test')

    return {"data": added_hotel}


@app.delete('/hotels/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_hotel(id: int) -> Response:
    deleted_hotel = Hotel.delete_hotel(id)

    if not deleted_hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Hotel with id {id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
