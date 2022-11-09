from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///sql_app.db'


engine = create_async_engine(
    SQL_ALCHEMY_DATABASE_URL, echo=True, connect_args={'check_same_thread': False}
)

async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base(engine)

from fast_api_recipes.models import Recipe
