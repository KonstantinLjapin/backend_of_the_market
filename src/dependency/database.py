from src.config import db_settings
from typing import AsyncGenerator
from fastapi import Request
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

Base: DeclarativeMeta = declarative_base()


def make_connection_string() -> str:
    """
    Make connection string to db
    """
    asyncpg_engine: str = "asyncpg"
    return (f"postgresql+{asyncpg_engine}://{db_settings.postgres_user}:{db_settings.postgres_password}@"
            f"{db_settings.postgres_host}:{db_settings.postgres_port}/{db_settings.postgres_db}")


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass


engine = create_async_engine(make_connection_string())
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


