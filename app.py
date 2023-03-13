import os
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.games

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class GameModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    price: float = Field(...)
    category: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Fable Anniversary",
                "price": 4.99,
                "category": "Video Game"
            }
        }


class UpdateGameModel(BaseModel):
    name: Optional[str]
    price: Optional[float]
    category: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Fable Anniversary",
                "price": 4.99,
                "category": "Video Game"
            }
        }


@app.post("/", response_description="Add new game", response_model=GameModel)
async def create_game(game: GameModel = Body(...)):
    game = jsonable_encoder(game)
    new_game = await db["games"].insert_one(game)
    created_game = await db["games"].find_one({"_id": new_game.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_game)


@app.get(
    "/", response_description="List all games", response_model=List[GameModel]
)
async def list_games():
    games = await db["games"].find().to_list(1000)
    return games


@app.get(
    "/{id}", response_description="Get a single game", response_model=GameModel
)
async def show_game(id: str):
    if (game := await db["games"].find_one({"_id": id})) is not None:
        return game

    raise HTTPException(status_code=404, detail=f"Game {id} not found")


@app.put("/{id}", response_description="Update a game", response_model=GameModel)
async def update_game(id: str, student: UpdateGameModel = Body(...)):
    game = {k: v for k, v in game.dict().items() if v is not None}

    if len(game) >= 1:
        update_result = await db["games"].update_one({"_id": id}, {"$set": student})

        if update_result.modified_count == 1:
            if (
                updated_game := await db["games"].find_one({"_id": id})
            ) is not None:
                return updated_game

    if (existing_game := await db["games"].find_one({"_id": id})) is not None:
        return existing_game

    raise HTTPException(status_code=404, detail=f"Game {id} not found")


@app.delete("/{id}", response_description="Delete a game")
async def delete_game(id: str):
    delete_result = await db["games"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Game {id} not found")
