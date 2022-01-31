from fastapi import FastAPI
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from auth.router import router as auth_router
from routers.data_clean import router as data_clean_router
from routers.lexicon import router as lexicon_router
from routers.kmeans import router as kmeans_router
from routers.svm import router as svm_router
from routers.mlp import router as mlp_router

app = FastAPI()
api_key_header = APIKeyHeader(name="Token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from auth.user import User, UserDB
from auth.authentication import get_current_user
from fastapi.params import Depends
@app.get("/protected-route", response_model=User)
async def protected_route(user: UserDB = Depends(get_current_user)):
    return User.from_orm(user)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(data_clean_router, prefix="/data_clean", tags=["Data Clean"], dependencies=[Depends(get_current_user)])
app.include_router(lexicon_router, prefix="/lexicon", tags=["Lexicon"], dependencies=[Depends(get_current_user)])
app.include_router(kmeans_router, prefix="/kmeans", tags=["k-means"], dependencies=[Depends(get_current_user)])
app.include_router(svm_router, prefix="/svm", tags=["svm"], dependencies=[Depends(get_current_user)])
app.include_router(mlp_router, prefix="/mlp", tags=["mlp"], dependencies=[Depends(get_current_user)])

TORTOISE_ORM = {
    "connections": {"default": "sqlite://csa.db"},
    "apps": {
        "models": {
            "models": ["models.data_clean", "auth.user", "auth.authentication", "aerich.models"],
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