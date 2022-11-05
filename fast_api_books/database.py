from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE_URL = 'sqlite://./sql_app.db'

engine = create_async_engine(
    SQL_ALCHEMY_DATABASE_URL, echo=True, check_same_thread=False
)
async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
session = async_session()

Base = declarative_base()
