from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel
from tortoise.models import Model
from tortoise import fields

class City(Enum):
    BAQ = 'BAQ'
    BOG = 'BOG'
    CLO = 'CLO'
    CUC = 'CUC'
    LTC = 'LTC'
    MDE = 'MDE'

class DataCleanTortoise(Model):
    id = fields.CharField(pk=True,max_length=20)
    content = fields.CharField(index=True, max_length=280)
    date = fields.DatetimeField(index=True)
    aprox_city = fields.CharEnumField(index=True, enum_type=City, max_length=3)
    clean_content = fields.CharField(max_length=280)

    class Meta:
        table = "data_clean"

class DataClean(BaseModel):
    id: str
    content: str
    date: datetime
    aprox_city: City
    clean_content: str

    class Config:
        orm_mode = True