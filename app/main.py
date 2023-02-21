from typing import List, Dict, Optional

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from random import randrange

hotels_data = [
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
        hotels_data.append(added_hotel)

        return added_hotel

    @staticmethod
    def find_hotel_idx(id: int) -> int | None:
        for i, hotel in enumerate(hotels_data):
            if hotel['id'] == id:
                return i

        return None

    @staticmethod
    def delete_hotel(id: int) -> Dict[str, str | int | bool] | None:
        deleted_hotel_idx = Hotel.find_hotel_idx(id)

        if deleted_hotel_idx != None:
            deleted_hotel = hotels_data.pop(deleted_hotel_idx)

            return deleted_hotel

        return None

    @staticmethod
    def get_data():
        return hotels_data

    @staticmethod
    def update_hotel(id, hotel, idx):
        updated_hotel = hotel.dict()
        hotels = Hotel.get_data()
        hotels[idx] = updated_hotel
        updated_hotel["id"] = id

        return updated_hotel


app = FastAPI()


@app.get('/hotels')
def get_all_hotels() -> Dict[str, List[Dict]]:
    hotels = Hotel.get_data()

    return {"data": hotels}


@app.get('/hotels/{id}')
def get_hotel_details(id: int) -> Dict | None:
    found_hotel_idx = Hotel.find_hotel_idx(id)

    if found_hotel_idx == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Hotel with id {id} not found")

    hotels = Hotel.get_data()

    return hotels[found_hotel_idx]


@app.post("/hotels", status_code=status.HTTP_201_CREATED)
def add_hotel(hotel: Hotel) -> Dict[str, dict]:
    added_hotel = hotel.add_hotel('Test')

    return {"data": added_hotel}


@app.put("/hotels/{id}", status_code=status.HTTP_200_OK)
def update_hotel_info(id: int, hotel: Hotel) -> Dict[str, Dict]:
    found_hotel_idx = Hotel.find_hotel_idx(id)

    if found_hotel_idx == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Hotel with id {id} not found")

    updated_hotel = Hotel.update_hotel(id, hotel, found_hotel_idx)

    return {"data": updated_hotel}


@app.delete('/hotels/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_hotel(id: int) -> Response:
    deleted_hotel = Hotel.delete_hotel(id)

    if not deleted_hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Hotel with id {id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
