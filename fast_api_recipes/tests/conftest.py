import asyncio
from typing import Generator, Callable

import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

from fast_api_recipes.database import Base
from fast_api_recipes.dependencies import get_async_session
from fast_api_recipes.main import app
from fast_api_recipes.models import Recipe

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///test.db"

PAYLOAD_DATA = [
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


@pytest_asyncio.fixture(scope="session")
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def db_engine() -> AsyncEngine:
    engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture()
async def session(db_engine: AsyncEngine) -> AsyncSession:
    async_session = sessionmaker(bind=db_engine, expire_on_commit=False, class_=AsyncSession)
    async with db_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        async with async_session(bind=connection) as session:
            yield session
            await session.rollback()


@pytest_asyncio.fixture()
async def seed_db(session: AsyncSession) -> None:
    data = PAYLOAD_DATA
    for recipe_data in data:
        new_recipe = Recipe(**recipe_data)
        session.add(new_recipe)
    await session.commit()


@pytest_asyncio.fixture()
def override_get_db(session: AsyncSession) -> Callable:
    async def _override_get_db():
        yield session

    return _override_get_db


@pytest_asyncio.fixture()
def test_app(override_get_db: Callable) -> FastAPI:
    app.dependency_overrides[get_async_session] = override_get_db
    return app


@pytest_asyncio.fixture()
async def client(seed_db, test_app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=test_app, base_url='http://localhost:8000') as ac:
        yield ac
