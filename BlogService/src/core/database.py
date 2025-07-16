from . import config
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from fastapi import Depends
from typing_extensions import Annotated
ASYNC_DB_URL = config.ASYNC_DB_URL #os.getenv('ASYNC_DB_URL')

Engine = create_async_engine(url=ASYNC_DB_URL)

# async_session = sessionmaker(bind=Engine, class_=AsyncSession, autoflush=False, autocommit=False, expire_on_commit=False)

async_session = async_sessionmaker(Engine, expire_on_commit=False, autoflush=False)
async def get_db():
    async with async_session() as session:
        yield session

session = Annotated[AsyncSession, Depends(get_db)]