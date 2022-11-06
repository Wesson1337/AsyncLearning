from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseRecipeSchema(BaseModel):
    title: str
    ingredients: str
    description: str
    cooking_time: int

    class Config:
        orm_mode = True


class RecipeSchemaIn(BaseRecipeSchema):
    ...


class RecipeSchemaPatch(BaseRecipeSchema):
    title: Optional[str]
    ingredients: Optional[str]
    description: Optional[str]
    cooking_time: Optional[int]


class RecipeSchemaOut(BaseRecipeSchema):
    id: int
    views_counter: int
    created: datetime
    updated: datetime
