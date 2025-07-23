from fastapi import APIRouter, Depends
from src.models.user import User
from src.schemas.user import UserRead, UserCreate, UserUpdate
from src.services.auth.dependencies import fastapi_users, auth_backend, current_active_user


router = APIRouter()

# JWT авторизация
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

# Все что связано с регистрацией, сбросом пароля и верификацией префиксы и теги собрал в одном месте
auth_router = APIRouter(prefix="/auth", tags=["auth"])
auth_router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
auth_router.include_router(fastapi_users.get_reset_password_router())
auth_router.include_router(fastapi_users.get_verify_router(UserRead))
router.include_router(auth_router)


@router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
