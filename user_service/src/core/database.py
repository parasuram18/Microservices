from . import config
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing_extensions import Annotated
from fastapi import Depends


ASYNC_DB_URL = config.ASYNC_DB_URL


engine = create_async_engine(url=ASYNC_DB_URL)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)

base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as db:
         yield db

Session = Annotated[AsyncSession, Depends(get_db)]