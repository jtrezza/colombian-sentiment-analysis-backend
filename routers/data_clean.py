from fastapi import APIRouter, HTTPException, status, Query
from fastapi.params import Depends

from models.data_clean import DataClean, DataCleanTortoise

router = APIRouter()

# Middlewares

async def pagination(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
) -> tuple[int, int]:
    capped_limit = min(100, limit)
    return (skip, capped_limit)

async def get_data_clean_or_404(id: int) -> DataCleanTortoise:
    return await DataCleanTortoise.get(id=id)


# Routes 

@router.get("/")
async def list_data_clean(pagination: tuple[int, int] = Depends(pagination)) -> list[DataClean]:
    skip, limit = pagination
    rows = await DataCleanTortoise.all().offset(skip).limit(limit)
    
    results = [DataClean.from_orm(row) for row in rows]

    return results


@router.post("/", response_model=DataClean, status_code=status.HTTP_201_CREATED)
async def create(row: DataClean) -> DataClean:
    row_tortoise = await DataCleanTortoise.create(**row.dict())
    
    return DataClean.from_orm(row_tortoise)


@router.get("/{id}", response_model=DataClean)
async def get_data_clean(row: DataClean = Depends(get_data_clean_or_404)) -> DataClean:    
    return DataClean.from_orm(row)
