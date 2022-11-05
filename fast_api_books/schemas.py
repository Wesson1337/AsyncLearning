from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseReceiptSchema(BaseModel):
    title: str
    views_counter: int
    ingredients: str
    description: str
    cooking_time: int
    created: Optional[datetime]
    updated: Optional[datetime]


class ReceiptSchemaIn(BaseReceiptSchema):
    ...


class ReceiptSchemaOut(BaseReceiptSchema):
    id: str
