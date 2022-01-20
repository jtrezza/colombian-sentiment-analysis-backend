# Python
from typing import Optional, List
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field

# FastAPI
from fastapi import FastAPI, status, Body, Query, Path

app = FastAPI()

# Models
class HairColor(Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    blonde = 'blonde'
    red = 'red'

class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='José'
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Trezza'
    )
    age: int = Field(
        ...,
        gt=0,
        le=115
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

class PublicPerson(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='José'
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Trezza'
    )

@app.get("/")
async def home():
    return {"Hello": "World"}

# Request and Response Body

@app.post('/person/new', response_model=PublicPerson,status_code=status.HTTP_201_CREATED)
async def create_person(person: Person = Body(...)):
    return person

# Validaciones: query parameters

@app.get('/person/detail')
async def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person's name. It's between 1 and 50 characters",
        example="Rocío"
    ),
    age: int = Query(
        ...,
        title="Person's age",
        description="This is the person's age. It's required",
        gt=17,
        example=25
    )
):
    return {name: age}

# Validaciones: Path
@app.get('/person/detail/{person_id}')
async def person_detail(
    person_id: int = Path(
        ...,
        title="Person's ID",
        description="This is the person's ID. It's required and must be greater than 0.",
        gt=0
    )
):
    return {person_id: "It exists!"}

# Validaciones: Request Body
@app.put('/person/{person_id}')
async def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person's ID",
        gt=0
    ),
    person: Person = Body(
        ...
    ),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results

a: List[int] = [1,2,3,4,5]
b: list[int] = [6,7,8,9,0]