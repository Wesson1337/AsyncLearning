from datetime import datetime

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


class ReceiptSchemaOut(BaseReceiptSchema):
    id: int
    views_counter: int
    created: datetime
    updated: datetime
