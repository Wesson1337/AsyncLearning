from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseReceiptSchema(BaseModel):
    title: str
    ingredients: str
    description: str
    cooking_time: int

    class Config:
        orm_mode = True


class ReceiptSchemaIn(BaseReceiptSchema):
    ...


class ReceiptSchemaPatch(BaseReceiptSchema):
    title: Optional[str]
    ingredients: Optional[str]
    description: Optional[str]
    cooking_time: Optional[int]


class ReceiptSchemaOut(BaseReceiptSchema):
    id: int
    views_counter: int
    created: datetime
    updated: datetime
