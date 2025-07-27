from __future__ import annotations

from sqlalchemy import Boolean, Column, Integer, String, ARRAY
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from src.dependency.roles import UserRole


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    roles = Column(ARRAY(String), nullable=False, default=[UserRole.USER.value])
