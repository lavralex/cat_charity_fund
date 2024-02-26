from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.schemas.base_db import BaseDB


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectCreate, BaseDB):
    pass