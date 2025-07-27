import uuid

from fastapi_users import schemas
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

from src.config.data_base import Base


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass