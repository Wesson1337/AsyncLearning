from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from fast_api_recipes.database import Base, engine


class Recipe(Base):
    __tablename__ = 'Recipe'
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(100))
    views_counter = Column(Integer, default=0)
    ingredients = Column(String(255))
    description = Column(Text)
    cooking_time = Column(Integer)
    created = Column(DateTime, default=datetime.now(), nullable=False)
    updated = Column(DateTime, default=datetime.now(), nullable=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
