from __future__ import annotations

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTableUUID


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass
