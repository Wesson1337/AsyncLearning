import os
from typing import List, Literal

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api_recipes.models import init_db
from fast_api_recipes.dependencies import get_async_session
from fast_api_recipes.schemas import RecipeSchemaOut, RecipeSchemaIn, RecipeSchemaPatch
from fast_api_recipes.services import get_all_recipes_db, create_new_recipe_db, get_certain_recipe_db, \
    patch_recipe_db, delete_recipe_db


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get('/recipes', response_model=List[RecipeSchemaOut])
async def get_all_recipes(
        session: AsyncSession = Depends(get_async_session)
) -> list[RecipeSchemaOut]:

    recipes = await get_all_recipes_db(session)
    return recipes


@app.post('/recipes', response_model=RecipeSchemaOut, status_code=201)
async def create_recipe(
        recipe: RecipeSchemaIn,
        session: AsyncSession = Depends(get_async_session)
) -> RecipeSchemaOut:

    new_recipe = await create_new_recipe_db(recipe, session)
    return new_recipe


@app.get('/recipes/{pk}', response_model=RecipeSchemaOut,
         responses={404: {"detail": "Not found"}})
async def get_certain_recipe(
        pk: int,
        session: AsyncSession = Depends(get_async_session)
) -> RecipeSchemaOut:

    recipe = await get_certain_recipe_db(pk, session)
    return recipe


@app.patch('/recipes/{pk}', response_model=RecipeSchemaOut)
async def patch_recipe(
        pk: int,
        recipe: RecipeSchemaPatch,
        session: AsyncSession = Depends(get_async_session)
) -> RecipeSchemaOut:

    updated_recipe = await patch_recipe_db(pk, recipe, session)
    return updated_recipe


@app.delete('/recipes/{pk}')
async def delete_recipe(
        pk: int,
        session: AsyncSession = Depends(get_async_session)
) -> dict[Literal["message"], str]:

    response = await delete_recipe_db(pk, session)
    return response
