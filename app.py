from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from routers.data_clean import router as data_clean_router
from routers.lexicon import router as lexicon_router
from routers.kmeans import router as kmeans_router

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data_clean_router, prefix="/data_clean", tags=["Data Clean"])
app.include_router(lexicon_router, prefix="/lexicon", tags=["Lexicon"])
app.include_router(kmeans_router, prefix="/kmeans", tags=["k-means"])

TORTOISE_ORM = {
    "connections": {"default": "sqlite://csa.db"},
    "apps": {
        "models": {
            "models": ["models.data_clean", "aerich.models"],
            "default_connection": "default",
        },
    },
}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)