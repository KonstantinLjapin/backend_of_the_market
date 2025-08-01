from fastapi import APIRouter, Depends

from src.dependency.models import User
from src.dependency.users import auth_backend, current_active_user, fastapi_users, is_user
from src.schemas.schema_user import UserCreate, UserRead, UserUpdate

auth_router = APIRouter()

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
auth_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
auth_router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
auth_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@auth_router.get("/authenticated-route")
async def user_dashboard(user: User = Depends(is_user())):
    return {"message": f"Добро пожаловать, {user.email}!"}



