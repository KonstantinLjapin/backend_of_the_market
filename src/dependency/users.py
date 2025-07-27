import uuid
from typing import Optional
from fastapi import Depends, Request, HTTPException, status
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase

from src.config import settings_authorization
from src.dependency.database import get_user_db
from src.dependency.models import User
from src.dependency.roles import UserRole

SECRET = settings_authorization.secret_key


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=settings_authorization.refresh_token_expire_minutes)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)


def required_roles(required_roles: list[UserRole]):
    async def checker(user: User = Depends(current_active_user)):
        # Преобразуем строковые роли в Enum для сравнения
        user_roles = [UserRole(role) for role in user.roles]

        # Проверяем наличие хотя бы одной из требуемых ролей
        if not any(role in user_roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав"
            )
        return user

    return checker


# Дополнительные проверки (возвращаем функции, а не объекты Depends)
def is_admin():
    return required_roles([UserRole.ADMIN])


def is_manager():
    return required_roles([UserRole.MANAGER])


def is_user():
    return required_roles([UserRole.USER])


def is_admin_or_manager():
    return required_roles([UserRole.ADMIN, UserRole.MANAGER])


def is_authenticated():
    """Проверка что пользователь просто аутентифицирован"""

    async def checker(user: User = Depends(current_active_user)):
        return user

    return Depends(checker)


def is_admin_or_owner(target_user_id: uuid.UUID):
    """Проверка что пользователь админ ИЛИ владелец ресурса"""

    async def checker(user: User = Depends(current_active_user)):
        user_roles = [UserRole(role) for role in user.roles]

        if UserRole.ADMIN in user_roles:
            return user

        if user.id == target_user_id:
            return user

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен"
        )

    return Depends(checker)