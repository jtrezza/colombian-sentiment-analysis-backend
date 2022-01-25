from datetime import datetime
from typing import Optional, cast

from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field

from tortoise import fields, timezone
from tortoise.models import Model
from tortoise.exceptions import DoesNotExist

from .password import verify_password, generate_token
from .user import UserDB, UserTortoise, get_expiration_date

class AccessToken(BaseModel):
    user_id: int
    access_token: str = Field(default_factory=generate_token)
    expiration_date: datetime = Field(default_factory=get_expiration_date)

    class Config:
        orm_mode = True

class AccessTokenTortoise(Model):
    access_token = fields.CharField(pk=True, max_length=255)
    user = fields.ForeignKeyField("models.UserTortoise", null=False)
    expiration_date = fields.DatetimeField(null=False)

    class Meta:
        table = "access_tokens"

async def get_current_user(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/token")),
) -> UserTortoise:
    try:
        access_token: AccessTokenTortoise = await AccessTokenTortoise.get(
            access_token=token, expiration_date__gte=timezone.now()
        ).prefetch_related("user")
        return cast(UserTortoise, access_token.user)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

async def authenticate(email: str, password: str) -> Optional[UserDB]:
    try:
        user = await UserTortoise.get(email=email)
    except DoesNotExist:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return UserDB.from_orm(user)


async def create_access_token(user: UserDB) -> AccessToken:
    access_token = AccessToken(user_id=user.id)
    access_token_tortoise = await AccessTokenTortoise.create(**access_token.dict())

    return AccessToken.from_orm(access_token_tortoise)