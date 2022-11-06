from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from database import Base


class Receipt(Base):
    __tablename__ = 'Receipt'
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(100))
    views_counter = Column(Integer, default=0)
    ingredients = Column(String(255))
    description = Column(Text)
    cooking_time = Column(Integer)
    created = Column(DateTime, default=datetime.now(), nullable=False)
    updated = Column(DateTime, default=datetime.now(), nullable=False)
