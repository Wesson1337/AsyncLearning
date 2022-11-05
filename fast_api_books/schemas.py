from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Receipt(BaseModel):
    title: str
    views_counter: int
    ingredients: str
    description: str
    cooking_time: int
    created: Optional[datetime]
    updated: Optional[datetime]
