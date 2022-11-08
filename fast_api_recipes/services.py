from datetime import datetime
from typing import Literal

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api_recipes.models import Recipe
from fast_api_recipes.schemas import RecipeSchemaIn, RecipeSchemaPatch


async def get_all_recipes_db(session: AsyncSession) -> list[Recipe]:
    result = await session.execute(select(Recipe).
                                   order_by(Recipe.views_counter.desc()).
                                   order_by(Recipe.cooking_time))
    return result.scalars().all()


async def create_new_recipe_db(recipe: RecipeSchemaIn, session: AsyncSession) -> Recipe:
    new_recipe = Recipe(**recipe.dict())
    session.add(new_recipe)
    await session.commit()
    return new_recipe


async def get_certain_recipe_db(pk: int, session: AsyncSession) -> Recipe:
    recipe = await session.get(Recipe, {'id': pk})
    if not recipe:
        raise HTTPException(status_code=404, detail='Recipe is not found')
    await _increment_views_counter(recipe, session)
    return recipe


async def _increment_views_counter(recipe: Recipe, session: AsyncSession) -> None:
    recipe.views_counter += 1
    await session.commit()


async def patch_recipe_db(pk: int, recipe: RecipeSchemaPatch, session: AsyncSession) -> Recipe:
    recipe_data = recipe.dict(exclude_unset=True)

    if not recipe_data:
        raise HTTPException(status_code=400, detail='Add at least 1 valid field to patch')

    stored_recipe = await session.get(Recipe, {'id': pk})

    if not stored_recipe:
        raise HTTPException(status_code=404, detail='Recipe is not found')

    for k, v in recipe_data.items():
        if k and v:
            setattr(stored_recipe, k, v)
    stored_recipe.updated = datetime.now()

    await session.commit()
    updated_recipe = stored_recipe
    return updated_recipe


async def delete_recipe_db(pk: int, session: AsyncSession) -> dict[Literal["message"], str]:
    recipe = await session.get(Recipe, {'id': pk})
    if not recipe:
        raise HTTPException(status_code=404, detail='Recipe is not found')
    await session.delete(recipe)
    await session.commit()
    return {"message": "done"}
