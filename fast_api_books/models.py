from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from database import Base


class Receipt(Base):
    __tablename__ = 'Receipt'
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(100))
    views_counter = Column(Integer)
    ingredients = Column(String(255))
    description = Column(Text)
    cooking_time = Column(Integer)
    created = Column(DateTime(), server_onupdate=datetime.now())
    updated = Column(DateTime(), onupdate=datetime.now())
