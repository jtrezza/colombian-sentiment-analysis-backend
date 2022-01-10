from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from routers.data_clean import router as data_clean_router

app = FastAPI()

app.include_router(data_clean_router, prefix="/data_clean", tags=["Data Clean"])

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