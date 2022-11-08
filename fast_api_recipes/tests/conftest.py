import pytest
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api_recipes.dependencies import get_async_session
from fast_api_recipes.main import get_app
from fast_api_recipes.models import Recipe


@pytest.fixture(scope='session')
async def test_session() -> AsyncSession:
    session = get_async_session()
    yield session
    await session.rollback()


@pytest.fixture(scope='session')
async def seed_db():
    data = [
        {
            'title': 'test_title',
            'ingredients': 'test_ingredients',
            'description': 'test_description',
            'cooking_time': 3
        },
        {
            'title': 'test2_title',
            'ingredients': 'test2_ingredients',
            'description': 'test2_description',
            'cooking_time': 4
        }
    ]
    session = test_session()
    for recipe_data in data:
        new_recipe = Recipe(**recipe_data)
        session.add(new_recipe)
    await session.commit()
